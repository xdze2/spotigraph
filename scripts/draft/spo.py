

from collections import Counter
from rich import print

from spotigraph.utils import get_related, get_followed_artists, Node, explore, Link


artists = set(
    Node.from_obj(art) for art in get_followed_artists()
)

print(artists)

root = Node(name='Matéo Langlois', id='5iAo2jptWeVCRvy2tzVdsA')
# root = Node(name='Sages comme des sauvages', id='3j2ckI4waH4C0E50srzHXj')
# root = Node(name='Arthur H', id='2nYkI1rHgPRp95pTmO9GZR')
# root = Node(name='Miossec', id='0wf6vuNqTvdRGrmpsPu2kW')
# root = Node(name='Bertrand Belin', id='5yFrjxlSd8zPqzCCNrOI5h')
# root = Node(name='Dooz Kawa', id='4z8LvfxawVZLoLR1KTUzQL')
# root = Node(name='Lucio Bukowski', id='2uNTCtTH48JmBT5b3PEgcW')
# root = Node(name='Anton Serra', id='4hP7MU4b6uUn1UZQblU9LI')

# 1st gen
new_artists, links = explore([root, ])

# 2nd gen
new_new_artists, second_gen_links = explore(new_artists)

print(len(new_new_artists), len(second_gen_links))



c = Counter(link[1] for link in second_gen_links)

print(c.most_common(10))
most_cited = c.most_common(1)[0][0]
print(most_cited)

to_exclude = set(link[0] for link in second_gen_links if link[1] == most_cited)
print(to_exclude)

c2 = Counter(link[1] for link in second_gen_links if link[0] not in to_exclude)

print(c2.most_common(5))