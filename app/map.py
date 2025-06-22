# ✅ app/map.py

import streamlit as st
from agent import get_google_maps_url

query = st.experimental_get_query_params().get("query", [""])[0]

st.title("📍 Nearby Hospitals")

if query:
    url = get_google_maps_url(query)
    st.markdown(f"🗺️ [Click to open map externally]({url})", unsafe_allow_html=True)
    st.components.v1.iframe(url, height=500)
else:
    st.warning("❗No query provided. Return to home and submit again.")
