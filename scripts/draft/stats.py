

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
        pop.append(related_obj.popularity)
        followers.append(related_obj.followers.total)

print(len(pop))
print(related_obj.followers)

plt.figure()
plt.hist(pop)
plt.xlabel('popularity')
plt.savefig('output/pop_hist.png')

plt.figure()
plt.hist(np.log(followers))
plt.xlabel('followers')
plt.savefig('output/followers_hist.png')