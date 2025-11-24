"""
Library View Module - User's Personal Content Library
"""
import streamlit as st
import sqlite3
from datetime import datetime
import re
import os


def convert_youtube_url(url):
    """Convert YouTube watch URL to embed URL for better compatibility"""
    if "youtube.com/watch" in url:
        match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in url:
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    return url


def load_video(path):
    """Load video from local file or URL with proper handling"""
    if path.startswith("http://") or path.startswith("https://"):
        return convert_youtube_url(path)
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Video file not found: {path}")
        return None
    except Exception as e:
        st.warning(f"Could not load video file: {e}")
        return path


def load_audio(path):
    """Load audio from local file or URL with proper handling"""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Audio file not found: {path}")
        return None
    except Exception as e:
        st.warning(f"Could not load audio file: {e}")
        return path


def library_view(user_id, role):
    """
    Display user's personal library with filters, sorting, and actions
    
    Args:
        user_id: Current user's ID
        role: User's role (student, practitioner, author)
    """
    st.header("📚 My Library")
    st.write("Your personal collection of videos, audio, and books.")
    
    # Filters and sorting
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.markdown("**Filters:**")
        filter_cols = st.columns(4)
        filter_video = filter_cols[0].checkbox("🎥 Video", value=True, key="filter_video")
        filter_audio = filter_cols[1].checkbox("🎵 Audio", value=True, key="filter_audio")
        filter_book = filter_cols[2].checkbox("📚 Book", value=True, key="filter_book")
        filter_all = filter_cols[3].checkbox("All", value=False, key="filter_all")
    
    with col2:
        sort_by = st.selectbox(
            "Sort by:",
            ["Date (Newest)", "Date (Oldest)", "Title (A-Z)", "Title (Z-A)", "Author"],
            key="sort_library"
        )
    
    with col3:
        view_mode = st.radio("View:", ["Grid", "List"], horizontal=True, key="view_mode")
    
    st.markdown("---")
    
    # Build filter query
    content_types = []
    if filter_all:
        content_types = ["video", "audio", "book", "movie"]
    else:
        if filter_video:
            content_types.append("video")
        if filter_audio:
            content_types.append("audio")
        if filter_book:
            content_types.extend(["book", "document"])
    
    # Get user's library content
    conn = sqlite3.connect("content_index.db")
    cursor = conn.cursor()
    
    # Query: Get content user has uploaded or purchased
    # For now, we show all content (Phase 1), but in Phase 2 this will filter by ownership
    if content_types:
        placeholders = ','.join('?' * len(content_types))
        query = f"""
            SELECT id, title, type, tags, path, added_at, author, description, uploaded_by
            FROM content 
            WHERE type IN ({placeholders})
        """
        cursor.execute(query, content_types)
    else:
        cursor.execute("SELECT id, title, type, tags, path, added_at, author, description, uploaded_by FROM content WHERE 1=0")
    
    results = cursor.fetchall()
    
    # Sort results
    if sort_by == "Date (Newest)":
        results = sorted(results, key=lambda x: x[5] or "", reverse=True)
    elif sort_by == "Date (Oldest)":
        results = sorted(results, key=lambda x: x[5] or "")
    elif sort_by == "Title (A-Z)":
        results = sorted(results, key=lambda x: x[1].lower())
    elif sort_by == "Title (Z-A)":
        results = sorted(results, key=lambda x: x[1].lower(), reverse=True)
    elif sort_by == "Author":
        results = sorted(results, key=lambda x: (x[6] or "").lower())
    
    # Display content
    if results:
        st.markdown(f"**{len(results)} items in your library**")
        st.markdown("")
        
        if view_mode == "List":
            # List view
            for item in results:
                display_library_item_list(item, user_id, role, conn)
        else:
            # Grid view (3 columns)
            cols = st.columns(3)
            for idx, item in enumerate(results):
                with cols[idx % 3]:
                    display_library_item_grid(item, user_id, role, conn)
    else:
        # Fallback message
        st.info("📭 No content yet — upload or purchase to begin")
        st.markdown("""
        **Get started:**
        - Switch to Practitioner role to upload content
        - Browse the search section for available content
        - Purchase or rent books and videos
        """)
    
    conn.close()


def display_library_item_list(item, user_id, role, conn):
    """Display library item in list view"""
    item_id, title, content_type, tags, path, added_at, author, description, uploaded_by = item
    
    # Icon based on type
    icon = {
        "video": "🎥",
        "audio": "🎵",
        "book": "📚",
        "document": "📄",
        "movie": "🎬"
    }.get(content_type, "📄")
    
    # Format date
    try:
        date_obj = datetime.fromisoformat(added_at)
        formatted_date = date_obj.strftime("%d %b %Y")
    except:
        formatted_date = added_at or "Unknown"
    
    # Ownership status
    is_owner = uploaded_by == user_id
    ownership_status = "Uploaded: Yes" if is_owner else "Purchased: Yes"
    
    # Container for item
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; margin-bottom: 15px; background-color: #fafafa;">
            <h4 style="margin: 0; color: #2E86AB;">{icon} {title}</h4>
            <p style="margin: 5px 0; color: #666; font-size: 14px;">
                <strong>Author:</strong> {author or "Unknown"} | <strong>Tags:</strong> {tags or "none"}<br>
                <strong>{ownership_status}</strong> | <strong>Date:</strong> {formatted_date}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        action_cols = st.columns([1, 1, 1, 3])
        
        with action_cols[0]:
            if content_type in ["video", "movie"]:
                play_key = f"play_{item_id}"
                if st.button("▶ Play", key=play_key, use_container_width=True):
                    st.session_state[f"playing_{item_id}"] = True
            elif content_type == "audio":
                play_key = f"play_audio_{item_id}"
                if st.button("▶ Play", key=play_key, use_container_width=True):
                    st.session_state[f"playing_{item_id}"] = True
            else:
                read_key = f"read_{item_id}"
                if st.button("📖 Read", key=read_key, use_container_width=True):
                    st.session_state[f"reading_{item_id}"] = True
        
        with action_cols[1]:
            if st.button("📥 Download", key=f"download_{item_id}", use_container_width=True):
                # Trigger download
                try:
                    with open(path, "rb") as f:
                        st.download_button(
                            label="Click to download",
                            data=f,
                            file_name=f"{title}.{path.split('.')[-1]}",
                            mime="application/octet-stream",
                            key=f"dl_btn_{item_id}"
                        )
                except:
                    st.error("File not found")
        
        with action_cols[2]:
            if is_owner and role in ["practitioner", "author"]:
                if st.button("🗑️ Remove", key=f"remove_{item_id}", use_container_width=True):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM content WHERE id = ?", (item_id,))
                    conn.commit()
                    st.success("Content removed!")
                    st.rerun()
        
        # Show content if play/read button was clicked
        if st.session_state.get(f"playing_{item_id}") or st.session_state.get(f"reading_{item_id}"):
            st.markdown("---")
            if content_type == "video" or content_type == "movie":
                # Case 1: YouTube link
                if "youtube.com" in path or "youtu.be" in path:
                    if "watch?v=" in path:
                        video_id = path.split("watch?v=")[-1].split("&")[0]
                        embed_url = f"https://www.youtube.com/embed/{video_id}"
                    elif "youtu.be" in path:
                        video_id = path.split("/")[-1]
                        embed_url = f"https://www.youtube.com/embed/{video_id}"
                    else:
                        embed_url = path
                    st.video(embed_url)
                # Case 2: Local file
                elif os.path.isfile(path):
                    try:
                        with open(path, "rb") as f:
                            st.video(f.read())
                    except Exception as e:
                        st.error(f"Could not open video file: {e}")
                # Case 3: Fallback
                else:
                    st.warning(f"Video unavailable. Path not found: {path}")
            elif content_type == "audio":
                # Case 1: URL
                if path.startswith("http://") or path.startswith("https://"):
                    st.audio(path)
                # Case 2: Local file
                elif os.path.isfile(path):
                    try:
                        with open(path, "rb") as f:
                            st.audio(f.read())
                    except Exception as e:
                        st.error(f"Could not open audio file: {e}")
                # Case 3: Fallback
                else:
                    st.warning(f"Audio unavailable. Path not found: {path}")
            else:
                st.markdown(f"**{title}**")
                st.markdown(f"*{description or 'No description available'}*")
                try:
                    with open(path, "rb") as f:
                        st.download_button(
                            label="📥 Download to read",
                            data=f,
                            file_name=f"{title}.pdf",
                            mime="application/pdf",
                            key=f"read_dl_{item_id}"
                        )
                except:
                    st.error("File not available")
        
        st.markdown("---")


def display_library_item_grid(item, user_id, role, conn):
    """Display library item in grid view (card format)"""
    item_id, title, content_type, tags, path, added_at, author, description, uploaded_by = item
    
    # Icon based on type
    icon = {
        "video": "🎥",
        "audio": "🎵",
        "book": "📚",
        "document": "📄",
        "movie": "🎬"
    }.get(content_type, "📄")
    
    # Format date
    try:
        date_obj = datetime.fromisoformat(added_at)
        formatted_date = date_obj.strftime("%d %b %Y")
    except:
        formatted_date = added_at or "Unknown"
    
    # Ownership status
    is_owner = uploaded_by == user_id
    
    # Card container
    with st.container():
        st.markdown(f"""
        <div style="border: 2px solid #2E86AB; border-radius: 10px; padding: 15px; margin-bottom: 20px; background-color: #f9fafb; min-height: 200px;">
            <div style="text-align: center; font-size: 48px; margin-bottom: 10px;">{icon}</div>
            <h4 style="margin: 5px 0; text-align: center; color: #2E86AB;">{title}</h4>
            <p style="margin: 5px 0; color: #666; font-size: 12px; text-align: center;">
                {author or "Unknown"}<br>
                {formatted_date}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons (stacked vertically in grid view)
        if content_type in ["video", "movie"]:
            if st.button("▶ Play", key=f"grid_play_{item_id}", use_container_width=True):
                st.session_state[f"grid_playing_{item_id}"] = True
        elif content_type == "audio":
            if st.button("▶ Play", key=f"grid_play_audio_{item_id}", use_container_width=True):
                st.session_state[f"grid_playing_{item_id}"] = True
        else:
            if st.button("📖 Read", key=f"grid_read_{item_id}", use_container_width=True):
                st.session_state[f"grid_reading_{item_id}"] = True
        
        if st.button("📥 Download", key=f"grid_download_{item_id}", use_container_width=True):
            try:
                with open(path, "rb") as f:
                    st.download_button(
                        label="⬇️",
                        data=f,
                        file_name=f"{title}.{path.split('.')[-1]}",
                        mime="application/octet-stream",
                        key=f"grid_dl_btn_{item_id}",
                        use_container_width=True
                    )
            except:
                st.error("File not found")
        
        if is_owner and role in ["practitioner", "author"]:
            if st.button("🗑️ Remove", key=f"grid_remove_{item_id}", use_container_width=True):
                cursor = conn.cursor()
                cursor.execute("DELETE FROM content WHERE id = ?", (item_id,))
                conn.commit()
                st.success("Removed!")
                st.rerun()
        
        # Show content in modal/expander if clicked
        if st.session_state.get(f"grid_playing_{item_id}") or st.session_state.get(f"grid_reading_{item_id}"):
            with st.expander(f"▶ {title}", expanded=True):
                if content_type == "video" or content_type == "movie":
                    # Case 1: YouTube link
                    if "youtube.com" in path or "youtu.be" in path:
                        if "watch?v=" in path:
                            video_id = path.split("watch?v=")[-1].split("&")[0]
                            embed_url = f"https://www.youtube.com/embed/{video_id}"
                        elif "youtu.be" in path:
                            video_id = path.split("/")[-1]
                            embed_url = f"https://www.youtube.com/embed/{video_id}"
                        else:
                            embed_url = path
                        st.video(embed_url)
                    # Case 2: Local file
                    elif os.path.isfile(path):
                        try:
                            with open(path, "rb") as f:
                                st.video(f.read())
                        except Exception as e:
                            st.error(f"Could not open video file: {e}")
                    # Case 3: Fallback
                    else:
                        st.warning(f"Video unavailable. Path not found: {path}")
                elif content_type == "audio":
                    # Case 1: URL
                    if path.startswith("http://") or path.startswith("https://"):
                        st.audio(path)
                    # Case 2: Local file
                    elif os.path.isfile(path):
                        try:
                            with open(path, "rb") as f:
                                st.audio(f.read())
                        except Exception as e:
                            st.error(f"Could not open audio file: {e}")
                    # Case 3: Fallback
                    else:
                        st.warning(f"Audio unavailable. Path not found: {path}")
                else:
                    st.markdown(description or "No description")
                    try:
                        with open(path, "rb") as f:
                            st.download_button(
                                label="📥 Download",
                                data=f,
                                file_name=f"{title}.pdf",
                                mime="application/pdf",
                                key=f"grid_read_dl_{item_id}"
                            )
                    except:
                        st.error("File not available")
