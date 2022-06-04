

from dataclasses import asdict

import altair as alt
import pandas as pd
from altair import datum
from rich import print as pprint
from spotigraph.apicall import get_audio_features, get_user_top_tracks


top_tracks = get_user_top_tracks(time_range='medium_term')
print(len(top_tracks))

# analys = spotify.track_audio_analysis(track_id)



df = pd.DataFrame.from_records(
    asdict(get_audio_features(track.id)) for track in top_tracks
)
    
print(df)





metrics = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
       'speechiness', 'tempo',  'valence'],


chart = alt.Chart(df).transform_window(
    index='count()'
).transform_fold(
    *metrics
).transform_joinaggregate(
     min='min(value)',
     max='max(value)',
     groupby=['key']
).transform_calculate(
    minmax_value=(datum.value-datum.min)/(datum.max-datum.min),
    mid=(datum.min+datum.max)/2
).mark_line().encode(
    x='key:N',
    y='minmax_value:Q',
    color='species:N',
    detail='index:N',
    opacity=alt.value(0.2),
    size=alt.value(2),
).properties(width=900)


chart.save('output/tracks_chart.html')
