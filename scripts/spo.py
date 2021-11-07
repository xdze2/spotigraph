

from rich import print

from spotigraph.utils import get_related, get_followed_artists, Node, explore


artists = set(
    Node.from_obj(art) for art in get_followed_artists()
)

# print(artists)

root = Node(name='Matéo Langlois', id='5iAo2jptWeVCRvy2tzVdsA')

new_artists, links = explore([root, ])

print(new_artists)

new_new_artists, new_links = explore(new_artists)

print(new_new_artists)
print(len(new_new_artists))