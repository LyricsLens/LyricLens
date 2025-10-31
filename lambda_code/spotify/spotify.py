import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import re

#shut up, dont care, womp womp
CLIENT_ID = '622c032e55de4204901f03aae8b8cb45'
CLIENT_SECRET = 'e2e4732c2f8342a3bc3af2883df70266'

# def get_token():
#     auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
#     r = requests.post("https://accounts.spotify.com/api/token",
#                       headers={"Authorization": f"Basic {auth}"},
#                       data={"grant_type":"client_credentials"}, timeout=10)
#     r.raise_for_status()
#     return r.json()["access_token"]

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

    tracks = []
    while results:
        for item in results["items"]:
            track = item.get("track")
            if track:
                name = track["name"]
                artists = ", ".join([artist["name"] for artist in track["artists"]])
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