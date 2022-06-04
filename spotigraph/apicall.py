import base64
import time
from typing import List

import requests
from diskcache import Cache

import tekore as tk
from tekore.model import AudioFeatures, FullArtist, FullTrack
from tekore.model import Image as TekoreImage
from tekore.model import ModelList

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
    print("get related for", art_id, end="\r")
    return SPOTIFY.artist_related_artists(art_id)


@CACHE.memoize()
def get_artist(artist_id: str) -> FullArtist:
    return SPOTIFY.artist(artist_id)


@CACHE.memoize()
def get_audio_features(track_id: str) -> AudioFeatures:
    return SPOTIFY.track_audio_features(track_id)


@CACHE.memoize(expire=24 * 60 * 60)
def get_user_top_tracks(time_range="medium_term") -> List[FullTrack]:
    return list(
        SPOTIFY.all_items(SPOTIFY.current_user_top_tracks(time_range=time_range))
    )


@CACHE.memoize()
def download_image(url: str):
    r = requests.get(url)
    return r.content


@CACHE.memoize()
def get_artist_top_tracks(artist_id: str):
    return list(SPOTIFY.all_items(SPOTIFY.artist_top_tracks(artist_id)))


def get_base64_image(image: TekoreImage) -> str:
    try:
        url = image.url
    except AttributeError:
        return ""

    content = download_image(url)
    base64_encoded_data = base64.b64encode(content)
    base64_message = base64_encoded_data.decode("utf-8")
    return f"data:image/jpg;base64,{base64_message}"


@CACHE.memoize(expire=24 * 60 * 60)
def search_artist(query: str, limit: int = None) -> List[FullArtist]:
    (artists,) = SPOTIFY.search(query, types=("artist",), limit=limit)
    return list(SPOTIFY.all_items(artists))
