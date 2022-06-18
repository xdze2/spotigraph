

from spotigraph.explore import get_first_gen, get_second_gen

from spotigraph.types import Artist
from spotigraph.network import build_links
from spotigraph.network import export_to_pajek, to_integer_indexed_graph


artist_id_a = "4ksCwAPgMi8rkQwwR3nMos"
artist_id_b = "2omAWwH1ZV9JYIyfMUQSgG"


second_gen_a = get_second_gen(artist_id_a)
second_gen_b = get_second_gen(artist_id_b)


jonction = second_gen_a & second_gen_b

print('Junction')
print('--------')
for art, count in jonction.most_common():
    print(f'{count: 3d}', art.name)




print('--------')
for (artA, countA), (artB, countB) in zip(second_gen_a.most_common(), second_gen_b.most_common()):
    print(f"{artA.name:>30}", f'{countA: 3d}', '-', f'{countB: 3d}', artB.name)


