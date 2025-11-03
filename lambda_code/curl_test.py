import requests


if __name__ == '__main__':
    # res = requests.get('https://5f7xe6x9ca.execute-api.us-east-1.amazonaws.com/dev/songs?playlist_url=https://open.spotify.com/playlist/5Ez74MIoh4pOSLFXhpwKdr?si=DWZs4p9RQwK3gA050AX9Ig&pi=u-SO_Jbus3TK2f')
    res = requests.get('https://5f7xe6x9ca.execute-api.us-east-1.amazonaws.com/dev/songs')

    print(res)
    print(res.content)