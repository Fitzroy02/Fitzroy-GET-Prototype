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


def render_phase_vi_dashboard(practitioner, badge_gate, curriculum_loader, annotation_logger):
    st.write("Phase VI dashboard loaded.")  # simple placeholder for integration


def main():
    st.set_page_config(page_title="GETS Studio", layout="wide")
    st.title("GETS Studio")

    # Initialize license registry in session state
    if "license_registry" not in st.session_state:
        # Load from JSON file if it exists
        if os.path.exists("license_registry.json"):
            with open("license_registry.json", "r") as f:
                st.session_state.license_registry = json.load(f)
        else:
            st.session_state.license_registry = []

    # Upload Section
    st.markdown("---")
    st.header("Upload File")

    with st.form("upload_form"):
        uploaded_file = st.file_uploader(
            "Select a file to upload",
            type=["pdf", "mp3", "mp4"]
        )

        title = st.text_input("Title")
        author = st.text_input("Author")
        access_type = st.selectbox("Access Type", [
            "Open",
            "Community",
            "Private"
        ])
        price = st.number_input("Price (£)", min_value=0.0, step=0.5)
        preview_pages = st.slider("Preview Pages", min_value=1, max_value=20, value=3)
        categories = st.multiselect("Categories", [
            "Education", "Art", "Community", "Heritage"
        ])

        submitted = st.form_submit_button("Upload")

    if submitted:
        new_license = {
            "title": title,
            "author": author,
            "access_type": access_type,
            "price": price,
            "allow_download": access_type == "Open",
            "preview_length": preview_pages,
            "scenario_tags": categories,
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
        
        st.success("File uploaded successfully!")
        st.write("**Title:**", title)
        st.write("**Author:**", author)
        st.write("**Access:**", access_type)
        st.write("**Price:** £", price)
        st.write("**Preview Pages:**", preview_pages)
        st.write("**Categories:**", ", ".join(categories))
        if uploaded_file:
            st.write("**File:**", uploaded_file.name)
            st.write("**File type:**", uploaded_file.type)
            st.write("**Saved to:**", save_path)
            
            # Live preview based on file type
            if uploaded_file.type == "application/pdf":
                st.markdown("### PDF Preview")
                uploaded_file.seek(0)  # Reset pointer
                base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf"></iframe>'
                st.markdown(pdf_display, unsafe_allow_html=True)
            
            elif uploaded_file.type.startswith("audio"):
                st.markdown("### Audio Preview")
                st.audio(uploaded_file)
            
            elif uploaded_file.type.startswith("video"):
                st.markdown("### Video Preview")
                st.video(uploaded_file)

    # Library Section
    if st.session_state.license_registry:
        st.markdown("---")
        st.header("Library of Works")
        
        # Filter by category
        filter_category = st.selectbox(
            "Filter by Category",
            ["All", "Education", "Art", "Community", "Heritage"]
        )
        
        def matches_category(entry, selected):
            if selected == "All":
                return True
            return selected in entry.get("scenario_tags", [])
        
        filtered_registry = [
            entry for entry in st.session_state.license_registry
            if matches_category(entry, filter_category)
        ]
        
        st.write(f"Showing {len(filtered_registry)} of {len(st.session_state.license_registry)} works")
        st.markdown("---")
        
        if not filtered_registry:
            st.info("No works match the selected category.")
        
        for item in filtered_registry:
            st.markdown(f"### {item['title']} by {item['author']}")
            st.write("**Access:**", item.get("license_type", "N/A"))
            st.write("**Price:** £", item["price"])
            st.write("**Preview Pages:**", item.get("preview_length", "N/A"))
            if item.get('filename'):
                st.write("**File:**", item['filename'])
            st.markdown("---")

    # Media Section
    st.markdown("---")
    st.header("Upload Audio or Video")

    # Upload audio or video
    audio_video_file = st.file_uploader(
        "Select an audio or video file",
        type=["mp3", "wav", "ogg", "mp4", "webm", "mov"],
        key="media_upload"
    )

    # Caption input
    caption = st.text_input("Caption")

    # Input method: local or remote
    source_type = st.radio("File Location", ["Local", "Remote"])

    if source_type == "Local":
        local_path = st.text_input("File Path")
        if local_path:
            if os.path.exists(local_path):
                st.success("Local file found.")
                st.audio(local_path)
            else:
                st.error("Local file not found. Check the path.")

    elif source_type == "Remote":
        remote_url = st.text_input("Remote URL")
        if remote_url:
            try:
                response = requests.get(remote_url)
                if response.status_code == 200:
                    st.success("Remote file reachable.")
                    st.audio(remote_url)
                else:
                    st.error(f"Remote file returned status code {response.status_code}.")
            except Exception as e:
                st.error(f"Error accessing remote file: {e}")

    # Test playback
    if st.button("Test Playback"):
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", format="audio/mp3")
        st.info("Playing test audio.")

    # Playback logic for uploaded media
    if audio_video_file is not None:
        file_type = audio_video_file.type
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with st.expander("Preview Uploaded Media"):
            if file_type.startswith("audio"):
                st.audio(audio_video_file)
            elif file_type.startswith("video"):
                st.video(audio_video_file)
            else:
                st.error("Unsupported file type. Please upload audio or video only.")

        # Display caption if provided
        if caption:
            st.write(f"**Caption:** {caption}")

        # Log upload
        st.write(f"Uploaded at: {timestamp}")

    # Reflection Section
    st.markdown("---")
    st.header("Pause and Reflect")
    st.write("Take a moment before sharing.")

    # Call the Phase VI renderer (placeholder)
    render_phase_vi_dashboard(None, None, None, None)

    # Timestamp Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<small><em>Generated on {timestamp}</em></small>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
