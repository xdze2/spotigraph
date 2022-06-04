import click

from spotigraph.apicall import search_artist


@click.command()
@click.argument("query_str")
@click.option("-n", "limit", help="Max number of results", default=5, show_default=True)
def search(query_str, limit: int = 5):
    """Use Spotify search API."""
    print(f'Make search request for "{query_str}"...')
    artists = search_artist(query_str, limit=limit)
    for arti in artists[:limit]:
        print(arti.id, arti.name)


if __name__ == "__main__":
    search()
