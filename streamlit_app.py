import streamlit as st
import os
import requests
from datetime import datetime


def render_phase_vi_dashboard(practitioner, badge_gate, curriculum_loader, annotation_logger):
    st.write("Phase VI dashboard loaded.")  # simple placeholder for integration


def main():
    st.set_page_config(page_title="GETS Studio V-1.6", layout="wide")
    st.title("GETS Studio V-1.6")
    st.subheader("A Civic Rehearsal Portal for Artists, Educators, and Ethical Thought Practitioners")

    # Lineage Badge
    st.markdown("""
    <div style="background-color:#f0f0f0;padding:10px;border-radius:5px;border-left:5px solid #4B0082;">
        <strong>🪶 Lineage Badge:</strong> Transmission authored by Fitzroy Brian Edwards (John Thought Hope).  
        This module is part of GETS Studio V-1.1: Echo Threshold, encoded for sonic integrity and civic embed.
    </div>
    """, unsafe_allow_html=True)

    scenario = st.sidebar.selectbox(
        "Choose a scenario",
        ["Ethical Pause", "Civic Rehearsal", "Legacy Stewardship"],
    )

    # DJ Stream Integrity Helper
    with st.expander("🎧 DJ Stream Integrity – Audio Troubleshooting"):
        st.markdown("""
        This module ensures your DJ stream resonates clearly. Use it to diagnose playback issues and uphold sonic integrity.

        **1. Is the file format supported?**  
        Streamlit supports MP3, WAV, and OGG formats. Other formats may not play.

        **2. Is the file too large or slow to load?**  
        Large files can cause delays or failures. Try a smaller audio clip to rule out bandwidth or loading issues.

        **3. Is your browser blocking autoplay or sound?**  
        Many browsers mute autoplay by default. Try pressing play manually or adjust your browser's sound settings.

        **4. Is the audio hosted locally or remotely?**  
        - If local: Double-check the file path (it must be accessible to the Streamlit server).  
        - If remote: Test the URL directly in your browser to ensure it works and is reachable.

        ---
        _Every stream is a civic gesture. Every sound, a transmission of care._
        """)

    # Upload audio file
    audio_file = st.file_uploader("🎵 Upload your audio file", type=["mp3", "wav", "ogg"])

    with st.expander("🔊 Test Audio Playback"):
        st.markdown("Click below to test if your browser can play audio.")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")

    # Input method: local or remote
    source_type = st.radio("📡 Is your audio hosted locally or remotely?", ["Local", "Remote"])

    if source_type == "Local":
        local_path = st.text_input("📁 Enter local file path (relative to Streamlit server)")
        if local_path:
            if os.path.exists(local_path):
                st.success("✅ Local file found and accessible.")
                st.audio(local_path)
            else:
                st.error("❌ Local file not found. Check the path and ensure it's accessible to the server.")

    elif source_type == "Remote":
        remote_url = st.text_input("🌐 Enter remote audio URL")
        if remote_url:
            try:
                response = requests.get(remote_url)
                if response.status_code == 200:
                    st.success("✅ Remote file reachable.")
                    st.audio(remote_url)
                else:
                    st.error(f"❌ Remote file returned status code {response.status_code}.")
            except Exception as e:
                st.error(f"❌ Error accessing remote file: {e}")

    # File size check (limit: 10MB)
    MAX_SIZE_MB = 10

    # Format validation
    if audio_file is not None:
        file_size_mb = audio_file.size / (1024 * 1024)
        st.markdown(f"📦 File size: `{file_size_mb:.2f} MB`")

        if file_size_mb > MAX_SIZE_MB:
            st.warning("⚠️ File may be too large. Try a smaller clip to rule out loading issues.")
        else:
            st.success("✅ File size is within optimal range.")

        if audio_file.name.endswith(('.mp3', '.wav', '.ogg')):
            st.success(f"✅ Format supported: {audio_file.name}")
            st.audio(audio_file, format=f"audio/{audio_file.name.split('.')[-1]}")
            # Playback prompt
            st.markdown("🔈 **Note:** Some browsers block autoplay. If you don't hear sound, press play manually or check your browser's sound settings.")
        else:
            st.error("❌ Unsupported format. Please upload MP3, WAV, or OGG.")

    # Call the Phase VI renderer (placeholder)
    render_phase_vi_dashboard(None, None, None, None)

    # Timestamp Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<small><em>Scaffolded on {timestamp} BST</em></small>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
