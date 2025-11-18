import streamlit as st
import os
import requests


def render_phase_vi_dashboard(practitioner, badge_gate, curriculum_loader, annotation_logger):
    st.write("Phase VI dashboard loaded.")  # simple placeholder for integration


def main():
    st.set_page_config(page_title="GETS Studio V-1.6", layout="wide")
    st.title("GETS Studio V-1.6")
    st.subheader("A Civic Rehearsal Portal for Artists, Educators, and Ethical Thought Practitioners")

    scenario = st.sidebar.selectbox(
        "Choose a scenario",
        ["Ethical Pause", "Civic Rehearsal", "Legacy Stewardship"],
    )

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


if __name__ == "__main__":
    main()
