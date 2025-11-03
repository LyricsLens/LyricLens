import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
import os
import logging

_logger = logging.getLogger(__name__)

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')

def extract_playlist_id(playlist_url):
    """Extracts the playlist ID from a Spotify playlist URL."""
    match = re.search(r"playlist/([a-zA-Z0-9]+)", playlist_url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid Spotify playlist URL.")

def get_playlist_tracks(playlist_url):
    """Returns a list of (song_name, artist_name) from a public playlist."""
    # Authenticate without user login (public data only)

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_id = extract_playlist_id(playlist_url)
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
        {}
        return {
            'title': song_title,
            'artist': artist_name,
            'lyrics': lyrics
        }
    except Exception as e:
        return {}


# === MULTITHREADING WRAPPER ===
def fetch_all_lyrics_concurrently(songs):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_song = {executor.submit(fetch_lyrics, title, artist): (title, artist) for title, artist in songs}

        for future in as_completed(future_to_song):
            title, artist = future_to_song[future]
            try:
                lyrics = future.result()
                if lyrics:
                    results.append(lyrics)
            except Exception as e:
                print(f"Failed to fetch {title}: {e}")
            time.sleep(0.3)  # small delay to avoid hammering Genius

    return results

def get_playlist_lyrics(playlist_url):
    _logger.info(('get playlist lyrics', playlist_url))
    songs = get_playlist_tracks(playlist_url)
    _logger.info(('found tracks', len(songs)))
    lyrics = fetch_all_lyrics_concurrently(songs)
    return lyrics
    if lyrics:
        return {'statusCode': 200, "body": json.dumps(lyrics)}
    return {'statusCode': 400, "body": json.dumps({"message": "Issue getting songs from playlist. Make sure the playlist is public and there are songs."})}

# def main():
#     playlist_url = 'https://open.spotify.com/playlist/1xp9QWsPelyEs1qLNBvMBe?si=96bae7b9fe654e07'
#     songs = get_playlist_tracks(playlist_url)

#     print(songs)

# if __name__=='__main__':
#     main()