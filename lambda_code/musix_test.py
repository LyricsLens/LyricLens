from bs4 import BeautifulSoup
import requests

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
print(soup)
# find the lyrics data.
cols = soup.findAll(class_="lyrics__content__ok", text=True)
if cols:
    lyrics = "\n".join(x.text for x in cols)
elif data := soup.find(class_="lyrics__content__warning", text=True):
    lyrics = data.get_text()
# finally print the lyrics.
print(lyrics)