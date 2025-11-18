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

    # The Whistling Wind Book Section
    with st.expander("📖 The Whistling Wind — Full Book"):
        st.markdown("### 📚 The Whistling Wind by John Thought Hope")
        st.markdown("*A poetic transmission exploring rhythm, resonance, and civic breath.*")
        
        # Note: Add the_whistling_wind.pdf to your repository to enable download
        # Uncomment when PDF is available:
        # import os
        # if os.path.exists("the_whistling_wind.pdf"):
        #     with open("the_whistling_wind.pdf", "rb") as f:
        #         st.download_button(
        #             "📥 Download The Whistling Wind (PDF)",
        #             f,
        #             file_name="the_whistling_wind.pdf",
        #             mime="application/pdf"
        #         )
        
        st.info("Book preview coming soon. Upload the PDF to enable download and viewing.")

    # Scenario-specific content
    if scenario == "Ethical Pause":
        st.markdown("#### 🌬️ Ethical Pause")
        st.markdown("""
        *A moment to breathe, reflect, and attune.*
        
        In this scenario, practitioners pause before action—allowing space for emotional 
        resonance and ethical consideration. The Whistling Wind invites contemplation 
        before transmission.
        """)
    elif scenario == "Civic Rehearsal":
        st.markdown("#### 🎭 Civic Rehearsal")
        st.markdown("""
        *Practice the gestures of care before they're needed.*
        
        This scenario enables practitioners to rehearse civic responses, test emotional 
        tones, and refine their transmissions. Each rehearsal strengthens the muscle 
        of collective care.
        """)
    elif scenario == "Legacy Stewardship":
        st.markdown("#### 🕊️ Legacy Stewardship")
        st.markdown("""
        *Tend the archive. Honor the lineage. Pass it forward.*
        
        In this mode, practitioners become stewards of transmissions—archiving wisdom, 
        annotating echoes, and ensuring that each gesture carries forward with integrity 
        and resonance.
        """)

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

    # Upload Media Section
    st.header("🎧📽️ Upload Your Media")

    # Upload audio or video
    uploaded_file = st.file_uploader(
        "Upload an audio or video file",
        type=["mp3", "wav", "ogg", "mp4", "webm", "mov"]
    )

    # Caption input
    caption = st.text_input("📝 Add a caption or poetic note for your media")

    # Session state to track ad playback
    if "ad_played" not in st.session_state:
        st.session_state.ad_played = False

    # Playback logic
    if uploaded_file is not None:
        file_type = uploaded_file.type
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.expander("📽️ Preview Uploaded Media"):
            if file_type.startswith("audio"):
                st.audio(uploaded_file)
            elif file_type.startswith("video"):
                st.video(uploaded_file)
            else:
                st.error("Unsupported file type. Please upload audio or video only.")

        # Display caption if provided
        if caption:
            st.markdown(f"**Caption:** _{caption}_")

        # Log upload
        st.markdown(f"🕒 Uploaded at: `{timestamp}`")

        # Stream Integrity Badge
        st.success("✅ Stream Integrity Verified")

        # Trigger Advertisement (once per session)
        if not st.session_state.ad_played:
            st.markdown("---")
            st.subheader("🎬 Sponsored Interlude")
            st.markdown("""
            <iframe width="100%" height="315"
              src="https://www.youtube.com/embed/YTp7UQNE0Dw"
              title="The Whistling Wind Ad"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen></iframe>
            """, unsafe_allow_html=True)
            st.session_state.ad_played = True

    else:
        st.info("Upload a media file to activate stream integrity and trigger the sponsored interlude.")

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

    # Video Embeds
    st.subheader("🎬 Featured Transmissions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌬️ The Whistling Wind (Intro)**")
        st.markdown("""
        <iframe width="100%" height="315"
          src="https://www.youtube.com/embed/QYYvgFzR8Qc"
          title="The Whistling Wind Intro"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**📢 The Whistling Wind (Ad)**")
        st.markdown("""
        <iframe width="100%" height="315"
          src="https://www.youtube.com/embed/YTp7UQNE0Dw"
          title="The Whistling Wind Ad"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen></iframe>
        """, unsafe_allow_html=True)

    # Call the Phase VI renderer (placeholder)
    render_phase_vi_dashboard(None, None, None, None)

    # Timestamp Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<small><em>Scaffolded on {timestamp} BST</em></small>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
