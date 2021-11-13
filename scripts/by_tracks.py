


# from diskcache import Cache
import tekore as tk

from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, NamedTuple, Tuple, List, Set
import time

from spotigraph.auth import load_token


spotify = tk.Spotify(load_token())
# cache = Cache("cache")



top_tracks = spotify.current_user_top_tracks(time_range='medium_term')

top_tracks = list(spotify.all_items(top_tracks))

# spotify.all_items(
# print(top_tracks)
print(type(top_tracks))
print(len(top_tracks))
# track_id = "4b3Z1LHSSOuaRP3z7NKJuA"
track_id = top_tracks[0].id
audio = spotify.track_audio_features(track_id)
# analys = spotify.track_audio_analysis(track_id)
