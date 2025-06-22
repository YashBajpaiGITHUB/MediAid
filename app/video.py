# ✅ app/video.py

import streamlit as st
from agent import get_youtube_video_url

query = st.experimental_get_query_params().get("query", [""])[0]

st.title("🎥 Demo First-Aid Tutorial")

if query:
    url = get_youtube_video_url(query)
    st.markdown(f"🔗 [Click to watch on YouTube]({url})", unsafe_allow_html=True)
    st.components.v1.iframe(url.replace("watch?v=", "embed/"), height=400)
else:
    st.warning("❗No query found. Go back to the home page.")
