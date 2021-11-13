

from typing import List
from collections import Counter

from .apicall import get_related
from .types import Artist


def get_first_gen(artist_id: str) -> List[Artist]:
    return [Artist.from_FullArtist(arti) for arti in get_related(artist_id)]


def get_second_gen(artist_id: str) -> Counter:

    related_first_gen = get_first_gen(artist_id)

    related_twice = Counter(related_first_gen)
    for artist in related_first_gen:

        related_twice.update(
            Artist.from_FullArtist(arti) for arti in get_related(artist.id)
        )

    return related_twice

