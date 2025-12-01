import streamlit as st
import os
import requests
from datetime import datetime
import base64
import json
import logging
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.DEBUG)


def get_license_badge(license_type):
    """Return emoji and tooltip for each license type"""
    badges = {
        "Open Civic Read": ("🌿", "This word is wind—free to move, free to meet."),
        "Scenario Access": ("🔍", "Only in pause, rehearsal, or legacy shall this be revealed."),
        "Stewarded Access": ("🕊️", "To read is to offer presence. To pay is to honor the breath."),
        "Downloadable License": ("📦", "This may be carried, but not copied. Steward it well."),
        "Consignment License": ("🏛️", "This rests in civic hands—placed, not posted.")
    }
    return badges.get(license_type, ("❔", "Unknown license type."))


def render_phase_vi_dashboard(practitioner, badge_gate, curriculum_loader, annotation_logger):
    st.write("Phase VI dashboard loaded.")  # simple placeholder for integration


def main():
    st.set_page_config(page_title="Civic Rehearsal Portal", layout="wide")
    st.title("Civic Rehearsal Portal")
    st.subheader("Upload your work, explore examples, and share with others.")

    # Initialize license registry in session state
    if "license_registry" not in st.session_state:
        # Load from JSON file if it exists
        if os.path.exists("license_registry.json"):
            with open("license_registry.json", "r") as f:
                st.session_state.license_registry = json.load(f)
        else:
            st.session_state.license_registry = []

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

    # Sidebar book upload
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📤 Upload The Whistling Wind")
    # sidebar_uploaded_file = st.sidebar.file_uploader("Upload your PDF", type=["pdf"], key="sidebar_book_upload")
    sidebar_uploaded_file = None

    if sidebar_uploaded_file is not None:
        st.sidebar.success("✅ Book uploaded successfully!")
        st.sidebar.download_button(
            "📥 Download The Whistling Wind",
            sidebar_uploaded_file,
            file_name="the_whistling_wind.pdf",
            mime="application/pdf"
        )

    # The Whistling Wind Book Section
    with st.expander("📖 The Whistling Wind — Full Book"):
        st.markdown("### 📚 The Whistling Wind by John Thought Hope")
        st.markdown("*A poetic transmission exploring rhythm, resonance, and civic breath.*")
        
        if sidebar_uploaded_file is not None:
            st.markdown("### 📖 The Whistling Wind (Live Preview)")
            # Reset file pointer to beginning
            sidebar_uploaded_file.seek(0)
            base64_pdf = base64.b64encode(sidebar_uploaded_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            # Check if PDF exists in repository
            if os.path.exists("the_whistling_wind.pdf"):
                with open("the_whistling_wind.pdf", "rb") as f:
                    st.download_button(
                        "📥 Download The Whistling Wind (PDF)",
                        f,
                        file_name="the_whistling_wind.pdf",
                        mime="application/pdf"
                    )
            else:
                st.info("📚 Upload the PDF in the sidebar to enable preview and download.")

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

    # Civic Licensing Framework
    st.markdown("---")
    st.markdown("## 🛡️ Civic Licensing Framework")

    with st.form("upload_form"):
        st.markdown("### 📤 Upload Your Work")
        uploaded_file = st.file_uploader(
            "Upload your file (PDF, MP3, MP4)",
            type=["pdf", "mp3", "mp4"]
        )

        st.markdown("### 🧾 Metadata")
        title = st.text_input("Title of the Work")
        author = st.text_input("Author / Steward")
        license_type = st.selectbox("License Type", [
            "Open Civic Read",
            "Scenario Access",
            "Stewarded Access",
            "Downloadable License",
            "Consignment License"
        ])
        price = st.number_input("Price (£)", min_value=0.0, step=0.5)
        allow_download = st.checkbox("Allow Download?")
        preview_length = st.slider("Preview Length (pages)", min_value=1, max_value=20, value=3)
        scenario_tags = st.multiselect("Scenario Tags", [
            "Ethical Pause", "Legacy Stewardship", "Civic Rehearsal",
            "Threshold", "Invocation", "Arrival"
        ])

        submitted = st.form_submit_button("Submit License")

    if submitted:
        new_license = {
            "title": title,
            "author": author,
            "license_type": license_type,
            "price": price,
            "allow_download": allow_download,
            "preview_length": preview_length,
            "scenario_tags": scenario_tags,
            "filename": uploaded_file.name if uploaded_file else None
        }
        
        # Save uploaded file to uploads directory
        if uploaded_file is not None:
            os.makedirs("uploads", exist_ok=True)
            save_path = os.path.join("uploads", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            new_license["file_path"] = save_path
        
        st.session_state.license_registry.append(new_license)
        
        # Save to JSON file
        with open("license_registry.json", "w") as f:
            json.dump(st.session_state.license_registry, f, indent=2)
        
        st.success("✅ License submitted successfully!")
        st.write("**Title:**", title)
        st.write("**Author:**", author)
        st.write("**License Type:**", license_type)
        st.write("**Price:** £", price)
        st.write("**Download Allowed:**", "Yes" if allow_download else "No")
        st.write("**Preview Length:**", preview_length, "pages")
        st.write("**Scenario Tags:**", ", ".join(scenario_tags))
        if uploaded_file:
            st.write("**File:**", uploaded_file.name)
            st.write("**File type:**", uploaded_file.type)
            st.write("**Saved to:**", save_path)
            
            # Live preview based on file type
            if uploaded_file.type == "application/pdf":
                st.markdown("### 📖 Live Book Preview")
                uploaded_file.seek(0)  # Reset pointer
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            elif uploaded_file.type.startswith("audio"):
                st.markdown("### 🎵 Audio Preview")
                st.audio(uploaded_file, format="audio/mp3")
            
            elif uploaded_file.type.startswith("video"):
                st.markdown("### 🎬 Video Preview")
                st.video(uploaded_file)

    # Display license registry
    if st.session_state.license_registry:
        st.markdown("---")
        st.markdown("## 📚 Registered Works")
        
        # Filter by scenario
        st.markdown("### 🔍 Filter by Scenario")
        selected_scenarios = st.multiselect(
            "Choose scenario(s) to explore",
            ["Ethical Pause", "Legacy Stewardship", "Civic Rehearsal", "Threshold", "Invocation", "Arrival"]
        )
        
        def matches_scenario(entry, selected):
            return any(tag in entry["scenario_tags"] for tag in selected)
        
        filtered_registry = [
            entry for entry in st.session_state.license_registry
            if not selected_scenarios or matches_scenario(entry, selected_scenarios)
        ]
        
        st.markdown(f"*Showing {len(filtered_registry)} of {len(st.session_state.license_registry)} works*")
        st.markdown("---")
        
        if not filtered_registry:
            st.info("🌬️ No works match the selected scenarios. Try a different combination or clear your filter.")
        
        for item in filtered_registry:
            emoji, tooltip = get_license_badge(item["license_type"])
            st.markdown(f"### {emoji} {item['title']} by {item['author']}")
            st.caption(f"**License:** {item['license_type']} — *{tooltip}*")
            st.write("**Price:** £", item["price"])
            st.write("**Download Allowed:**", "Yes" if item["allow_download"] else "No")
            st.write("**Preview Length:**", item["preview_length"])
            st.write("**Scenario Tags:**", ", ".join(item["scenario_tags"]))
            if item.get('filename'):
                st.write("**File:**", item['filename'])
            st.markdown("---")

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
    
    # Load media manifest
    if os.path.exists("media_config.json"):
        with open("media_config.json") as f:
            manifest = json.load(f)
        
        # UI: Select transmission type
        choice = st.radio("Choose your transmission:", ["Intro", "Ad", "Loop"])
        
        # Cue ritual
        if st.button("Begin Transmission"):
            if choice == "Intro":
                st.video(manifest["intro"]["video"])
                if os.path.exists(manifest["intro"]["text"]):
                    with open(manifest["intro"]["text"]) as f:
                        st.markdown(f.read())
            elif choice == "Ad":
                st.video(manifest["ad"]["video"])
                if os.path.exists(manifest["ad"]["text"]):
                    with open(manifest["ad"]["text"]) as f:
                        st.markdown(f.read())
            elif choice == "Loop":
                if os.path.exists(manifest["loop"]["audio"]):
                    st.audio(manifest["loop"]["audio"])
                    st.markdown("Ambient loop playing. Let the wind speak.")
        
        # Optional: Display cover image
        if os.path.exists(manifest["cover"]["image"]):
            st.image(manifest["cover"]["image"], caption="Whistling Wind Cover", use_column_width=True)
    else:
        # Fallback to original layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🌬️ The Whistling Wind (Intro)**")
            st.video("media/ww_intro_clip.mp4")
            if os.path.exists("media/ww_intro_text.txt"):
                st.markdown(open("media/ww_intro_text.txt").read())
        
        with col2:
            st.markdown("**📢 The Whistling Wind (Ad)**")
            st.video(os.path.join("media", "ww_ad_clip.mp4"))

    # Call the Phase VI renderer (placeholder)
    render_phase_vi_dashboard(None, None, None, None)

    # Timestamp Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<small><em>Scaffolded on {timestamp} BST</em></small>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
