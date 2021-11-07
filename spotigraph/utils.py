

from diskcache import Cache
import tekore as tk

from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, NamedTuple, Tuple, List, Set
import time

from .auth import load_token


spotify = tk.Spotify(load_token())
cache = Cache("cache")


@cache.memoize()
def get_followed_artists():
    followed_artists = spotify.followed_artists()
    return list(spotify.all_items(followed_artists))


@cache.memoize()
def get_related(art_id):
    time.sleep(1)
    return spotify.artist_related_artists(art_id)



class Node(NamedTuple):
    name: str
    id: str

    @classmethod
    def from_obj(cls, artist_obj):
        return cls(
            artist_obj.name,
            artist_obj.id
        )


class Link(NamedTuple):
    node: Node
    is_related_to: Node


def explore(artists: Iterable[Node]) -> Tuple[Set[Node], Set[Link]]:
    new_artists = set()
    links = set()
    for node in artists:
        for is_related in get_related(node.id):
            related = Node.from_obj(is_related)
            link = Link(node, related)
            links.add(link)
            if related not in artists:
                new_artists.add(related)
    return new_artists, links
