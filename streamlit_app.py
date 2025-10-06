import streamlit as st
from datetime import datetime

# Lineage Badge
st.markdown("""
<div style="background-color:#f0f0f0;padding:10px;border-radius:5px;border-left:5px solid #4B0082;">
    <strong>🪶 Lineage Badge:</strong> Transmission authored by Fitzroy Brian Edwards (John Thought Hope).  
    This module is part of GETS Studio V-1.1: Echo Threshold, encoded for sonic integrity and civic embed.
</div>
""", unsafe_allow_html=True)

# DJ Stream Integrity Helper
with st.expander("🎧 DJ Stream Integrity – Audio Troubleshooting"):
    st.markdown("""
    This module ensures your DJ stream resonates clearly. Use it to diagnose playback issues and uphold sonic integrity.

    **1. Is the file format supported?**  
    Streamlit supports MP3, WAV, and OGG formats. Other formats may not play.

    **2. Is the file too large or slow to load?**  
    Large files can cause delays or failures. Try a smaller audio clip to rule out bandwidth or loading issues.

    **3. Is your browser blocking autoplay or sound?**  
    Many browsers mute autoplay by default. Try pressing play manually or adjust your browser’s sound settings.

    **4. Is the audio hosted locally or remotely?**  
    - If local: Double-check the file path (it must be accessible to the Streamlit server).  
    - If remote: Test the URL directly in your browser to ensure it works and is reachable.

    ---
    _Every stream is a civic gesture. Every sound, a transmission of care._
    """)

# Embedded DJ Video Stream (replace with your actual video URL)
video_url = "https://your-hosted-video-link.com/dj_mix.mp4"
st.video(video_url)

# Timestamp Footer
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<small><em>Scaffolded on {timestamp} BST</em></small>", unsafe_allow_html=True)