# app/main.py

import streamlit as st
from agent import get_first_aid_response, get_youtube_video_url
import base64
import urllib.parse
import os
from fpdf import FPDF
import streamlit.components.v1 as components

st.set_page_config(page_title="MediAid", layout="centered")
st.markdown("""
    <style>
    body {
        background-color: #fffaf5;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 1.5em;
    }
    .card-box {
        border: 2px solid #f00;
        border-radius: 12px;
        padding: 20px;
        background-color: #fff0f0;
        margin: 1em 0;
    }
    .video-frame, .map-frame {
        width: 100%;
        height: 400px;
        border: none;
        border-radius: 8px;
    }
    .download-box {
        padding: 1em;
        border: 1px dashed #777;
        background-color: #fefefe;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🩺 MediAid</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Offline AI Assistant for Emergency First-Aid Help</div>", unsafe_allow_html=True)

# Emergency call shortcuts (India)
st.markdown("""
<div class='card-box'>
    <strong>📞 Emergency Contacts (India):</strong><br><br>
    ☎️ <a href="tel:112">112 - National Emergency Number</a><br>
    🚑 <a href="tel:102">102 - Ambulance (Medical Emergency)</a><br>
    🚓 <a href="tel:100">100 - Police Helpline</a><br>
    🔥 <a href="tel:101">101 - Fire Brigade</a>
</div>
""", unsafe_allow_html=True)

# Query input
query = st.text_input("💬 Describe the emergency situation:", placeholder="e.g. burn injury, fracture in finger")

if query:
    with st.spinner("🫀 Finding the best first-aid solution..."):
        response = get_first_aid_response(query)
        st.success("✅ Suggested Action:")
        st.info(response)

        # PDF Download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Emergency: {query}\n\nAdvice: {response}")
        pdf_path = f"fa_{query.replace(' ', '_')}.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="FirstAid_{query}.pdf">📦 Download First-Aid Advice as PDF</a>'
            st.markdown(f"<div class='download-box'>{href}</div>", unsafe_allow_html=True)

        os.remove(pdf_path)

        # Video Search
        st.markdown("### 📍 Demo First-Aid Tutorials")
        video_url = get_youtube_video_url(query)
        if video_url:
            st.markdown(f"<a href='{video_url}' target='_blank'><div class='card-box'>🎬 Watch Tutorial in New Tab</div></a>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Couldn't find a relevant tutorial video.")

        # Ask user to manually detect their location
        st.markdown("### 📍 Locate Nearby Hospitals")
        if st.button("📍 Detect My Location and Show Hospitals"):
            components.html(f"""
            <html>
            <body>
            <script>
            navigator.geolocation.getCurrentPosition(
                function(position) {{
                    var lat = position.coords.latitude;
                    var lon = position.coords.longitude;
                    var query = "{query}";
                    var mapUrl = "https://www.google.com/maps/search/?api=1&query=hospitals+near+" + lat + "," + lon + "+for+" + encodeURIComponent(query);
                    window.location.href = mapUrl;
                }},
                function(error) {{
                    alert("❌ Location permission denied or unavailable.");
                }}
            );
            </script>
            </body>
            </html>
            """, height=200)

# Mobile Compatibility Note
st.markdown("""
    <style>
    @media only screen and (max-width: 768px) {
        .main-title { font-size: 2rem; }
        .sub-title { font-size: 1rem; }
        .video-frame, .map-frame { height: 300px; }
    }
    </style>
""", unsafe_allow_html=True)
