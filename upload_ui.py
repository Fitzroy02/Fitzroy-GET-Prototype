"""
Upload UI Module - Content Upload Interface for Practitioners and Authors
"""
import streamlit as st
from datetime import datetime
import os
from pathlib import Path


def upload_interface(user_id, role):
    """
    Display upload interface with three sections: Video, Audio, and Books/Documents
    
    Args:
        user_id: Current user's ID
        role: User's role (practitioner, author)
    """
    st.header("📤 Upload Content")
    st.write("Upload videos, audio, or documents to your library.")
    
    # Create three-column layout for Video/Audio/Book loaders
    st.markdown("---")
    
    # Top row: Video and Audio loaders side by side
    col1, col2 = st.columns(2)
    
    with col1:
        video_loader(user_id, role)
    
    with col2:
        audio_loader(user_id, role)
    
    st.markdown("---")
    
    # Bottom row: Book/Document loader (full width)
    book_loader(user_id, role)


def video_loader(user_id, role):
    """Video upload section"""
    st.subheader("🎥 Video Loader")
    
    with st.container():
        st.markdown("""
        <div style="border: 2px solid #2E86AB; border-radius: 10px; padding: 20px; background-color: #f9fafb;">
        """, unsafe_allow_html=True)
        
        # File uploader
        video_file = st.file_uploader(
            "Upload Video",
            type=["mp4", "mov", "avi", "mkv"],
            key="video_uploader",
            help="Supported formats: MP4, MOV, AVI, MKV. Max size: 500MB"
        )
        
        # Metadata fields
        st.markdown("**Metadata**")
        video_title = st.text_input("Title", key="video_title", placeholder="Enter video title")
        video_author = st.text_input("Author", value=user_id, key="video_author")
        video_tags = st.text_input("Tags", key="video_tags", placeholder="e.g., training, demo, tutorial")
        video_desc = st.text_area("Description (optional)", key="video_desc", placeholder="Brief description of the video")
        
        # Preview window
        if video_file is not None:
            st.markdown("**Preview**")
            st.video(video_file)
            
            # File info
            st.caption(f"File: {video_file.name} ({video_file.size / (1024*1024):.2f} MB)")
        
        # Upload button
        if st.button("📤 Upload Video", key="upload_video_btn", type="primary"):
            if video_file and video_title:
                upload_content(
                    file=video_file,
                    title=video_title,
                    author=video_author,
                    tags=video_tags,
                    description=video_desc,
                    content_type="video",
                    user_id=user_id
                )
                st.success(f"✅ Video '{video_title}' uploaded successfully!")
            else:
                st.error("❌ Please provide a file and title.")
        
        st.markdown("</div>", unsafe_allow_html=True)


def audio_loader(user_id, role):
    """Audio upload section"""
    st.subheader("🎵 Audio Loader")
    
    with st.container():
        st.markdown("""
        <div style="border: 2px solid #2E86AB; border-radius: 10px; padding: 20px; background-color: #f9fafb;">
        """, unsafe_allow_html=True)
        
        # File uploader
        audio_file = st.file_uploader(
            "Upload Audio",
            type=["mp3", "wav", "aac", "m4a"],
            key="audio_uploader",
            help="Supported formats: MP3, WAV, AAC, M4A. Max size: 100MB"
        )
        
        # Metadata fields
        st.markdown("**Metadata**")
        audio_title = st.text_input("Title", key="audio_title", placeholder="Enter audio title")
        audio_author = st.text_input("Author", value=user_id, key="audio_author")
        audio_tags = st.text_input("Tags", key="audio_tags", placeholder="e.g., podcast, lecture, music")
        audio_desc = st.text_area("Description (optional)", key="audio_desc", placeholder="Brief description of the audio")
        
        # Preview window
        if audio_file is not None:
            st.markdown("**Preview**")
            st.audio(audio_file)
            
            # File info
            st.caption(f"File: {audio_file.name} ({audio_file.size / (1024*1024):.2f} MB)")
        
        # Upload button
        if st.button("📤 Upload Audio", key="upload_audio_btn", type="primary"):
            if audio_file and audio_title:
                upload_content(
                    file=audio_file,
                    title=audio_title,
                    author=audio_author,
                    tags=audio_tags,
                    description=audio_desc,
                    content_type="audio",
                    user_id=user_id
                )
                st.success(f"✅ Audio '{audio_title}' uploaded successfully!")
            else:
                st.error("❌ Please provide a file and title.")
        
        st.markdown("</div>", unsafe_allow_html=True)


def book_loader(user_id, role):
    """Book/Document upload section"""
    st.subheader("📚 Book/Document Loader")
    
    with st.container():
        st.markdown("""
        <div style="border: 2px solid #2E86AB; border-radius: 10px; padding: 20px; background-color: #f9fafb;">
        """, unsafe_allow_html=True)
        
        # File uploader
        doc_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "docx", "txt", "epub"],
            key="doc_uploader",
            help="Supported formats: PDF, DOCX, TXT, EPUB. Max size: 50MB"
        )
        
        # Metadata fields in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Metadata**")
            doc_title = st.text_input("Title", key="doc_title", placeholder="Enter document title")
            doc_author = st.text_input("Author", value=user_id, key="doc_author")
            doc_tags = st.text_input("Tags", key="doc_tags", placeholder="e.g., textbook, guide, reference")
        
        with col2:
            st.markdown("**Additional Info**")
            doc_desc = st.text_area("Description", key="doc_desc", placeholder="Brief description of the document", height=100)
            
            # Author-specific fields
            if role == "author":
                doc_institution = st.text_input("Institution", key="doc_institution", placeholder="University/Organization")
                doc_license = st.selectbox("License", 
                    ["All Rights Reserved", "CC BY", "CC BY-SA", "CC BY-NC", "Public Domain"],
                    key="doc_license"
                )
        
        # Preview/Download window
        if doc_file is not None:
            st.markdown("**Preview**")
            
            # File info
            st.caption(f"File: {doc_file.name} ({doc_file.size / (1024*1024):.2f} MB)")
            
            # Download button for preview
            st.download_button(
                label="📥 Download Preview",
                data=doc_file,
                file_name=doc_file.name,
                mime="application/octet-stream",
                key="preview_download"
            )
        
        # Upload button
        if st.button("📤 Upload Document", key="upload_doc_btn", type="primary", use_container_width=True):
            if doc_file and doc_title:
                upload_content(
                    file=doc_file,
                    title=doc_title,
                    author=doc_author,
                    tags=doc_tags,
                    description=doc_desc,
                    content_type="book",
                    user_id=user_id
                )
                st.success(f"✅ Document '{doc_title}' uploaded successfully!")
            else:
                st.error("❌ Please provide a file and title.")
        
        st.markdown("</div>", unsafe_allow_html=True)


def upload_content(file, title, author, tags, description, content_type, user_id):
    """
    Save uploaded file and add metadata to database
    
    Args:
        file: Uploaded file object
        title: Content title
        author: Content author
        tags: Comma-separated tags
        description: Content description
        content_type: Type of content (video, audio, book)
        user_id: User who uploaded the content
    """
    import sqlite3
    
    # Create uploads directory structure
    upload_dir = Path("uploads") / content_type + "s"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
    file_ext = Path(file.name).suffix
    filename = f"{timestamp}_{safe_title}{file_ext}"
    file_path = upload_dir / filename
    
    # Save file to disk
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    # Add metadata to database
    conn = sqlite3.connect("content_index.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO content (title, type, tags, path, added_at, author, description, uploaded_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        content_type,
        tags,
        str(file_path),
        datetime.now().isoformat(),
        author,
        description,
        user_id
    ))
    
    conn.commit()
    conn.close()
    
    return str(file_path)


def update_content_schema():
    """Update database schema to support comprehensive content metadata"""
    import sqlite3
    
    conn = sqlite3.connect("content_index.db")
    cursor = conn.cursor()
    
    # Check if columns exist, if not add them
    cursor.execute("PRAGMA table_info(content)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Legacy columns
    if "author" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN author TEXT")
    if "description" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN description TEXT")
    if "uploaded_by" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN uploaded_by TEXT")
    
    # New comprehensive metadata columns
    if "user_role" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN user_role TEXT DEFAULT 'student'")
    if "source" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN source TEXT DEFAULT 'local_file'")
    if "url" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN url TEXT")
    if "purchase_status" not in columns:
        cursor.execute("ALTER TABLE content ADD COLUMN purchase_status TEXT DEFAULT 'uploaded'")
    
    conn.commit()
    conn.close()
