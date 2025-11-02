import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import time


GENIUS_TOKEN = 'Lr9kZzpIy4Tlod-MoELEvjGvNXzeMgCyxO_yRzFqeJtINkj8zJUWuM37K6-WGPIw'

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
        
        return {
            'title': song_title,
            'artist': artist_name,
            'lyrics': lyrics_div.text.strip()
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
                results.append(lyrics)
            except Exception as e:
                print(f"Failed to fetch {title}: {e}")
            time.sleep(0.3)  # small delay to avoid hammering Genius

    return results

def main():
    songs = [('Foundations', 'Unveil The Strength'), ('Agony', 'Silent Theory'), ('All I Know', 'Five Finger Death Punch')]

    for title, author in songs:
        result = fetch_lyrics(title, author)
        print(result)

if __name__ == '__main__':
    main()