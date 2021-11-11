


# from diskcache import Cache
import tekore as tk

from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, NamedTuple, Tuple, List, Set
import time

from spotigraph.auth import load_token


spotify = tk.Spotify(load_token())
# cache = Cache("cache")



top_tracks = spotify.current_user_top_tracks(time_range='medium_term', limit=20, offset=0)
# spotify.all_items(
print(top_tracks)


track_id = "4b3Z1LHSSOuaRP3z7NKJuA"
audio = spotify.track_audio_features(track_id)
analys = spotify.track_audio_analysis(track_id)
