import requests


if __name__ == '__main__':
    res = requests.get('https://ird5gn5hv9.execute-api.us-east-1.amazonaws.com/dev/songs')
    # res = requests.get('https://ird5gn5hv9.execute-api.us-east-1.amazonaws.com/dev/images')

    print(res)
    print(res.content)