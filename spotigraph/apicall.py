

import time
import base64
import requests

import tekore as tk
from tekore.model import ModelList, FullArtist
from diskcache import Cache

from .auth import load_token


SPOTIFY = tk.Spotify(load_token())
CACHE = Cache("cache")


@CACHE.memoize()
def get_followed_artists():
    followed_artists = SPOTIFY.followed_artists()
    return list(SPOTIFY.all_items(followed_artists))


@CACHE.memoize()
def get_related(art_id: str) -> ModelList[FullArtist]:
    time.sleep(0.8)
    print('get related for', art_id, end='\r')
    return SPOTIFY.artist_related_artists(art_id)


@CACHE.memoize()
def get_artist(artist_id: str) -> FullArtist:
    return SPOTIFY.artist(artist_id)


@CACHE.memoize()
def download_image(url: str):
    r = requests.get(url)
    return r.content

def get_base64_image(url):
    content = download_image(url)
    base64_encoded_data = base64.b64encode(content)
    base64_message = base64_encoded_data.decode('utf-8')
    return f"data:image/jpg;base64,{base64_message}"


