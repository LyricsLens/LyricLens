import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.parse
import json
import time
import random
import logging
import asyncio
import aiohttp

_logger = logging.getLogger(__name__)

CLIENT_ID = '622c032e55de4204901f03aae8b8cb45'
CLIENT_SECRET = 'e2e4732c2f8342a3bc3af2883df70266'
GENIUS_TOKEN = 'LvVgUY1EnbzspBCfeCOfH2ZudhwSpt-YYaeiSy7afQI-XUU6X4UvST4mdT1SUo_0'
YOUTUBE_BASE = "https://lyrics.lewdhutao.my.eu.org/v2/youtube/lyrics"
MM_BASE = "https://lyrics.lewdhutao.my.eu.org/v2/musixmatch/lyrics"

def extract_playlist_id(playlist_url):
    """Extracts the playlist ID from a Spotify playlist URL."""
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Spotify playlist URL.")

def get_playlist_tracks(playlist_id):
    """Returns a list of (song_name, artist_name) from a public playlist."""
    # Authenticate without user login (public data only)

    auth_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET,     
        cache_handler=spotipy.cache_handler.CacheFileHandler(cache_path="/tmp/.cache-spotify")
    )   
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # playlist_id = extract_playlist_id(playlist_url)
    results = sp.playlist_items(playlist_id)

    tracks: list[tuple[str, str]] = []
    while results:
        for item in results["items"]:
            track = item.get("track")
            if track:
                name = track["name"]
                artists = track['artists'][0]['name']
                tracks.append((name, artists))

        # Handle pagination
        if results["next"]:
            results = sp.next(results)
        else:
            results = None

    return tracks

def fetch_lyrics(song_title, artist_name):
    """
    Search Genius for a song and return lyrics text.
    """
    headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}
    search_url = "https://api.genius.com/search"
    query = f"{song_title} {artist_name}"

    try:
        res = requests.get(search_url, headers=headers, params={"q": query}, timeout=10)
        res.raise_for_status()
        data = res.json()

        hits = data["response"]["hits"]
        if not hits:
            return {}

        song_path = hits[0]["result"]["path"]
        song_url = f"https://genius.com{song_path}"

        page = requests.get(song_url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")
        lyrics_div = soup.find_all("div", {"data-lyrics-container": "true"})[0]
        if not lyrics_div:
            return {}
        
        for child in lyrics_div.find_all("div", {"data-exclude-from-selection": "true"}):
            child.decompose() 

        for br in lyrics_div.find_all("br"):
            br.replace_with("\n")
        lyrics = lyrics_div.text.strip()

        if not lyrics:
            return {}
        return {
            'title': song_title,
            'artist': artist_name,
            'lyrics': lyrics
        }
    except Exception as e:
        return {}

class RateLimitedError(Exception):
    pass

def _encode_params(title: str, artist: str) -> str:
    return f"title={urllib.parse.quote_plus(title)}&artist={urllib.parse.quote_plus(artist)}"

async def fetch_json(session: aiohttp.ClientSession, url: str, *, max_retries=5, base_delay=0.5, timeout=10):
    """
    Fetch JSON with retries on 429/5xx. Exponential backoff + jitter.
    """
    attempt = 0
    while True:
        try:
            async with session.get(url, timeout=timeout) as r:
                if r.status == 429:
                    # surface as special error to trigger backoff
                    raise RateLimitedError("429 Too Many Requests")
                if 500 <= r.status < 600:
                    raise RuntimeError(f"Server error {r.status}")
                r.raise_for_status()
                return await r.json()
        except (RateLimitedError, aiohttp.ClientError, asyncio.TimeoutError, RuntimeError) as e:
            attempt += 1
            if attempt > max_retries:
                raise
            # decorrelated jitter backoff
            delay = min(30.0, random.uniform(0, 1) + base_delay * (2 ** (attempt - 1)))
            await asyncio.sleep(delay)

async def fetch_one_song(session, sem, title, artist, cache):
    key = (title.strip().lower(), artist.strip().lower())
    if key in cache:
        return cache[key]

    params = _encode_params(title, artist)

    async with sem:
        # Try primary (YouTube) first
        yt_url = f"{YOUTUBE_BASE}?{params}"
        try:
            data = await fetch_json(session, yt_url)
            lyrics = data.get("data", {}).get("lyrics")
            if lyrics:
                cache[key] = {"title": title, "artist": artist, "lyrics": lyrics}
                return cache[key]
        except Exception:
            # If it's a hard error, we still try fallback below
            pass

    # If no lyrics from YT, try Musixmatch (but still bounded by sem)
    async with sem:
        mm_url = f"{MM_BASE}?{params}"
        try:
            data_mm = await fetch_json(session, mm_url)
            lyrics_mm = data_mm.get("data", {}).get("lyrics")
            if lyrics_mm:
                cache[key] = {"title": title, "artist": artist, "lyrics": lyrics_mm}
                return cache[key]
        except Exception:
            pass

    # Nothing worked
    cache[key] = None
    return None

async def fetch_all_lyrics_concurrently(songs, *, max_concurrency=6, timeout=10):
    """
    songs: iterable of (title, artist)
    Returns: list of dicts with title, artist, lyrics
    """
    # Deduplicate upfront to reduce host pressure
    seen = set()
    deduped = []
    for t, a in songs:
        key = (t.strip().lower(), a.strip().lower())
        if key not in seen:
            seen.add(key)
            deduped.append((t, a))

    sem = asyncio.Semaphore(max_concurrency)
    cache = {}

    connector = aiohttp.TCPConnector(limit=0)  # let semaphore govern concurrency
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_one_song(session, sem, t, a, cache) for (t, a) in deduped]
        results = await asyncio.gather(*tasks, return_exceptions=False)

    # Map results back to original list order (including duplicates if present)
    out = []
    cache_for_lookup = {(t.strip().lower(), a.strip().lower()): res for (t, a), res in zip(deduped, results)}
    for t, a in songs:
        res = cache_for_lookup.get((t.strip().lower(), a.strip().lower()))
        if res:
            out.append(res)

    return out

def get_playlist_lyrics_async(playlist_id, *, max_concurrency=6):
    _logger.info(('get playlist lyrics', playlist_id))
    songs = get_playlist_tracks(playlist_id)
    _logger.info(('found tracks', len(songs)))
    # with open('playlist_results_example.json', 'r', encoding='utf-8') as file:
    #     lyrics = json.loads(file.read())['body']
    lyrics = fetch_all_lyrics_concurrently(songs)
    return lyrics

async def main():
    # playlist_url = 'https://open.spotify.com/playlist/5Ez74MIoh4pOSLFXhpwKdr'
    playlist_id = '0OpvByCWDSDxjakpIvIoVc'
    songs = get_playlist_tracks(playlist_id)
    lyrics = await get_playlist_lyrics_async(playlist_id)

    print(json.dumps(lyrics))
    # print(songs)

if __name__=='__main__':
    asyncio.run(main())