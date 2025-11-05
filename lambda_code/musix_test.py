from bs4 import BeautifulSoup
import requests
import json

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
SONG_LINK = 'https://www.musixmatch.com/lyrics/Josephine-Foster/Child-of-God'


def get_soup(url: str) -> BeautifulSoup:
    """
    Utility function which takes a url and returns a Soup object.
    """
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


# def get_url(title, artist):


# build bs4 soup object.
soup = get_soup(SONG_LINK)
# print(soup)
# find the lyrics data.
text = soup.find(id="__NEXT_DATA__").text
# print(data)
data = json.loads(text)
print(data['props']['pageProps']['data']['trackInfo']['data']['lyrics']['body'])

# if cols:
#     lyrics = "\n".join(x.text for x in cols)
# elif data := soup.find(class_="lyrics__content__warning", text=True):
#     lyrics = data.get_text()
# finally print the lyrics.
# print(lyrics)