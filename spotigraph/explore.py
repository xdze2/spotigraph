

from .apicall import get_related
from .types import Artist


from collections import Counter


def get_second_gen(artist_id: str) -> Counter:

    artist_id = "0wf6vuNqTvdRGrmpsPu2kW"
    related_first_gen = [Artist.from_FullArtist(arti) for arti in get_related(artist_id)]

    related_twice = Counter(related_first_gen)
    for artist in related_first_gen:

        related_twice.update(
            Artist.from_FullArtist(arti) for arti in get_related(artist.id)
        )

    return related_twice