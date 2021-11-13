
from dataclasses import dataclass, field, asdict
from typing import NamedTuple, List

from tekore.model import ModelList, FullArtist
from tekore.model import Image as TekoreImage

from .apicall import get_base64_image


def select_image(images: List[TekoreImage], target_size: int) -> TekoreImage:
    if not images:
        return None
    elif len(images) == 1:
        return images[0]
    else:
        squares = [
            image
            for image in images
            if image.width == image.height
        ]
        if len(squares) > 1:
            return min(
                squares,
                key = lambda im: abs(im.width - target_size)
            )
        else:
            return min(
                images,
                key = lambda im: abs(im.width - target_size)
            )


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
            image=get_base64_image(select_image(full_artist.images, 100))
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