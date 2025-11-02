import spotify
import genius
import json
def get_playlist_lyrics(playlist_url):
    songs = spotify.get_playlist_tracks(playlist_url)
    lyrics = genius.fetch_all_lyrics_concurrently(songs)
    # song = songs[0]
    # lyrics = genius.fetch_lyrics(song[0], song[1])
    print_text = [json.dumps(song_data) for song_data in lyrics]
    print('\n'.join(print_text))

if __name__ == '__main__':
    url = 'https://open.spotify.com/playlist/5Ez74MIoh4pOSLFXhpwKdr?si=DWZs4p9RQwK3gA050AX9Ig&pi=u-SO_Jbus3TK2f'
    get_playlist_lyrics(url)