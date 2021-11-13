

from spotigraph.apicall import search_artist



import click

@click.command()
@click.argument('query')
@click.option('-n', default=5, show_default=True)
def search(query, n: int=5):
    artists = search_artist(query, limit=n)
    for arti in artists[:n]:
        print(arti.name, arti.id)


if __name__ == '__main__':
    search()



