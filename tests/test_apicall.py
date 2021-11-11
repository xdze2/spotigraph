
from spotigraph.apicall import get_related, get_artist
from spotigraph.types import Artist


def test_get_related():
    artist_id = "0wf6vuNqTvdRGrmpsPu2kW"

    related = get_related(artist_id)

    print('-')
    print(type(related), '-')
    print(related)
    assert len(related) > 1


def test_get_artist():
    artist_id = "0wf6vuNqTvdRGrmpsPu2kW"

    full_artist = get_artist(artist_id)
    artist = Artist.from_FullArtist(full_artist)

    print(artist, hash(artist))
    assert hash(artist) != 0
    assert len(artist.image) > 0 
