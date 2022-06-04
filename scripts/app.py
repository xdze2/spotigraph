import streamlit as st

from spotigraph.apicall import search_artist
from spotigraph.types import select_image


st.title("app")


def add_to_selected(*args, **kwargs):
    st.write(args, kwargs)
    if "selected" in st.session_state:
        st.session_state["selected"].append(args)
    else:
        st.session_state["selected"] = [args]


def reset_selected():
    st.write("reset")
    st.session_state["selected"] = list()
    st.experimental_rerun()


if "selected" not in st.session_state or len(st.session_state["selected"]) == 0:

    #     st.session_state["selected"] = list()
    #     st.session_state.query = ""

    query = st.text_input("Search an artist", key="query")
    if not query:
        st.warning("Please input a name.")
        st.stop()
    else:
        st.warning(f"{query}")

    with st.spinner(text="Query in progress..."):
        answers = search_artist(query, limit=10)

    st.subheader("Results")
    cols = st.columns(5)
    for k, artist in enumerate(answers[:10]):
        image = select_image(artist.images, target_size=168)
        with cols[k % len(cols)]:
            st.image(image.url, caption=artist.name, width=100)
            st.button("select", key=artist.id, on_click=add_to_selected, args=(artist,))

else:
    #     st.warning('selected')
    st.subheader("Selected:")
    st.write(st.session_state["selected"])

    if st.button("clear", key="reset"):
        reset_selected()
