import requests


if __name__ == '__main__':
    res = requests.get('https://ird5gn5hv9.execute-api.us-east-1.amazonaws.com/dev/songs')
    # res = requests.get('https://ird5gn5hv9.execute-api.us-east-1.amazonaws.com/dev/images')
# https://open.spotify.com/playlist/5Ez74MIoh4pOSLFXhpwKdr?si=DWZs4p9RQwK3gA050AX9Ig&pi=u-SO_Jbus3TK2f
    print(res)
    print(res.content)