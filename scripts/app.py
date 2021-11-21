

import streamlit as st
from spotigraph.apicall import search_artist
from spotigraph.types import select_image

st.title('app')


if 'selected' not in st.session_state:
    st.session_state['selected'] = list()
    st.session_state.query = ''

def add_to_selected(*args, **kwargs):
    st.write(args, kwargs)

query = st.text_input('what', key='query')

if not query:
    st.stop()

with st.spinner(text="Query in progress..."):
    answers = search_artist(query)

cols = st.columns(3)
for k, artist in enumerate(answers):
    image = select_image(artist.images, target_size=168)
    with cols[k % len(cols)]:
        st.image(image.url, caption=artist.name, width=100)
        st.button('yo', key=artist.id, on_click=add_to_selected, args=(artist, ))

st.write(st.session_state['selected'])