import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import re

#Please don't hack me
CLIENT_ID = '622c032e55de4204901f03aae8b8cb45'
CLIENT_SECRET = 'e2e4732c2f8342a3bc3af2883df70266'

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

def main():
    playlist_url = 'https://open.spotify.com/playlist/1xp9QWsPelyEs1qLNBvMBe?si=96bae7b9fe654e07'
    songs = get_playlist_tracks(playlist_url)

    print(songs)

if __name__=='__main__':
    main()