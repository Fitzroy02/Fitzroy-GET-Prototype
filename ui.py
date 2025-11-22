# ui.py
import streamlit as st
from datetime import datetime
def show_header():
    st.set_page_config(page_title="Media & Scenario App", layout="wide")
    st.title("📖 Media & Scenario App")
def show_upload_forms():
    st.sidebar.header("Upload Files")
    sidebar_book_file = st.sidebar.file_uploader("Upload a book (PDF)", type=["pdf"])
    media_file = st.sidebar.file_uploader("Upload media (audio/video)", type=["mp3", "mp4"])
    return sidebar_book_file, media_file
def show_footer():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    st.markdown(f"---\nGenerated at {now}")