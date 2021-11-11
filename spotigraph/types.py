from dataclasses import dataclass, field, asdict
from typing import NamedTuple, List
from tekore.model import ModelList, FullArtist
from .apicall import get_base64_image

@dataclass(unsafe_hash=True)
class Artist:
    id: str = field(compare=True, hash=True)
    name: str = field(compare=False)
    popularity: int = field(compare=False)
    image: str = field(compare=False, default=None, repr=False)

    @classmethod
    def from_FullArtist(cls, full_artist: FullArtist) -> 'Artist':
        return cls(
            full_artist.id,
            full_artist.name,
            full_artist.popularity,
            image=get_base64_image(full_artist.images[2].url)
        )

    def asdict(self):
        return asdict(self)


def test_artist_type():
    a = Artist('56', '12', 44)
    b = Artist('56', '01012', 44)
    c = Artist('5116', '01012', 44)

    assert a == b
    assert a != c


class Link(NamedTuple):
    node: Artist
    is_related_to: Artist