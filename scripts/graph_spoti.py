

# -----------
#  First gen
# -----------

artists = set(
    Node.from_obj(art) for art in get_followed_artists()
)

new_artists, links = explore(artists)


print('len artists', len(artists))
print('len link', len(links))
print('len new_artists', len(new_artists))

# -------------
#  Seconde gen
# -------------
# import random
# new_artists2, links2 = explore(random.sample(new_artists, 20))
# print('len artists', len(new_artists))
# print('len link', len(links2))
# print('len new_artists', len(new_artists2))


# -------
#  Graph
# -------
from itertools import islice

print('--- graph ---')

artists_dict = {
    art.id: art
    for art in artists
}

# Add 2nd gen artiste
for cache_key in islice(cache.iterkeys(), None):
    if len(cache_key) != 2 or cache_key[0] != '__main__.get_related': continue
    for related_obj in cache[cache_key]:
        related = Node.from_obj(related_obj)
        artists_dict[related.id] = related

print('len(artists_dict)', len(artists_dict))

links = set()
for cache_key in islice(cache.iterkeys(), None):
    if len(cache_key) != 2 or cache_key[0] != '__main__.get_related': continue
    node = artists_dict[cache_key[1]]
    for related_obj in cache[cache_key]:
        related = Node.from_obj(related_obj)
        link = Link(node, related)
        links.add(link)

print(len(links))

artist_idx = {
    art.id: idx
    for idx, art in enumerate(sorted(artists_dict.values(), key=lambda x:x[1]))
}


output_path = 'output/graph.pajek'
Path(output_path).parent.mkdir(exist_ok=True, parents=True)

max_slice = None

import unicodedata
import re


with open(output_path, 'w') as f:

    f.write(f'*Vertices {len(artist_idx)}\n')
    for art_id, idx in islice(artist_idx.items(), max_slice):
        artist_name = artists_dict[art_id].name
        artist_name = unicodedata.normalize('NFKD', artist_name)
        artist_name = re.sub('\W+','', artist_name)
        f.write(f'{idx} "{artist_name}"\n')

    f.write('\n')
    f.write(f'*Edges {len(links)}\n')
    for node_a, node_b in islice(links, max_slice):
        f.write(f'{artist_idx[node_a.id]} {artist_idx[node_b.id]}\n')

#     links = set()
#     for node in artists:
#         for is_related in get_related(node.id):
#             related = Node.from_obj(is_related)
#             link = Link(node, related)
#             links.add(link)
#             if related not in artists:
#                 new_artists.add(related)


# related = get_related('6J434ZmyHxFcBjHXAZL9QY')
# related = get_related('2X2ePjwsB7PMG1FbbbLK6C')


