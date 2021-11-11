

import numpy as np

from diskcache import Cache
from itertools import islice
import matplotlib.pyplot as plt

cache = Cache("cache")

from spotigraph.utils import get_related

missings = set()
for cache_key in islice(cache.iterkeys(), None):
    if len(cache_key) != 2 or cache_key[0] != '__main__.get_related': continue
    for related_obj in cache[cache_key]:

        related_cache_key = get_related.__cache_key__(related_obj.id)

        if related_cache_key not in cache:
            missings.add((
                related_obj.id,
                related_obj.name,
                related_obj.popularity
            ))


print(len(missings))


missings = sorted(missings, key=lambda x:x[2], reverse=True)

print(missings[:5])

# for missing in missings[:20]:
#     get_related(missing[0])
