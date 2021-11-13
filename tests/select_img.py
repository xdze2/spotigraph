from spotigraph.explore import get_first_gen
from spotigraph.types import Artist


from spotigraph.apicall import get_related


from spotigraph.types import select_image


import numpy as np

from diskcache import Cache
from itertools import islice
import matplotlib.pyplot as plt

cache = Cache("cache")


pop = []
followers = []
for cache_key in islice(cache.iterkeys(), None):
    if len(cache_key) != 2 or cache_key[0] != '__main__.get_related': continue
    for related_obj in cache[cache_key]:
        
        try:
            image = select_image(related_obj.images, 100)
        except ValueError:
            print('err')
            print([img for img in related_obj.images])
            raise
