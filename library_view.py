"""
Library View Module - User's Personal Content Library
"""
import streamlit as st
import sqlite3
from datetime import datetime
import re
import os
import base64


def get_image_base64(image_path):
    """Convert image file to base64 string for inline display"""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""


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
            SELECT id, title, type, tags, path, added_at, author, description, uploaded_by, cover_image
            FROM content 
            WHERE type IN ({placeholders})
        """
        cursor.execute(query, content_types)
    else:
        cursor.execute("SELECT id, title, type, tags, path, added_at, author, description, uploaded_by, cover_image FROM content WHERE 1=0")
    
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
    item_id, title, content_type, tags, path, added_at, author, description, uploaded_by, cover_image = item
    
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
    
    # Cover style based on type
    cover_style = {
        "video": ("🎥", "#FF6B6B", "Video"),
        "audio": ("🎵", "#4ECDC4", "Audio"),
        "book": ("📚", "#95E1D3", "Book"),
        "document": ("📄", "#F38181", "Document"),
        "movie": ("🎬", "#AA96DA", "Movie")
    }
    icon, bg_color, type_label = cover_style.get(content_type, ("📄", "#CCCCCC", "File"))
    
    # Container with horizontal cover layout
    with st.container():
        # Show actual cover image if available, otherwise use gradient + icon
        if cover_image and os.path.isfile(cover_image):
            cover_html = f'<img src="data:image/png;base64,{get_image_base64(cover_image)}" style="width: 100%; height: 100%; object-fit: cover;">'
        else:
            cover_html = f'<div style="width: 100%; height: 100%; background: linear-gradient(135deg, {bg_color} 0%, {bg_color}CC 100%); display: flex; align-items: center; justify-content: center; font-size: 40px;">{icon}</div>'
        
        st.markdown(f"""
        <div style="border: 2px solid #2E86AB; border-radius: 10px; overflow: hidden; margin-bottom: 15px; background-color: #ffffff;">
            <div style="display: flex; flex-direction: row; align-items: stretch; min-height: 100px;">
                <!-- Cover Image Section -->
                <div style="flex: 0 0 100px; overflow: hidden;">
                    {cover_html}
                </div>
                <!-- Content Section -->
                <div style="flex: 1; padding: 12px 15px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-weight: 600; font-size: 15px; color: #2E86AB; margin-bottom: 4px;">
                        Title: {title}
                    </div>
                    <div style="font-size: 13px; color: #666; margin-bottom: 3px;">
                        Author: {author or "Unknown"}
                    </div>
                    <div style="font-size: 11px; color: #999;">
                        {type_label} • Added {formatted_date} • {tags or "No tags"}
                    </div>
                </div>
            </div>
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
    """Display library item in grid view (visual card format with cover image)"""
    item_id, title, content_type, tags, path, added_at, author, description, uploaded_by, cover_image = item
    
    # Icon/Cover based on type - Updated color palette
    cover_style = {
        "video": ("🎥", "#EF4444", "Video"),      # Red
        "audio": ("🎵", "#10B981", "Audio"),      # Green
        "book": ("📚", "#8B5CF6", "Book"),        # Purple
        "document": ("📄", "#F59E0B", "Document"), # Amber
        "movie": ("🎬", "#EF4444", "Movie")       # Red
    }
    icon, bg_color, type_label = cover_style.get(content_type, ("📄", "#9CA3AF", "File"))
    
    # Format date
    try:
        date_obj = datetime.fromisoformat(added_at)
        formatted_date = date_obj.strftime("%d %b %Y")
    except:
        formatted_date = added_at or "Unknown"
    
    # Ownership status
    is_owner = uploaded_by == user_id
    
    # Card container with vertical layout: Cover → Title → Author → Button
    with st.container():
        # Inject design system CSS with Roboto typography and color palette
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;1,400&display=swap');
        
        /* Card container styling */
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]) {
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 16px;
            background-color: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stImage"]):hover {
            box-shadow: 0 4px 12px rgba(30,64,175,0.15);
            transform: translateY(-2px);
        }
        
        /* Typography - Roboto family */
        div[data-testid="stMarkdownContainer"] p {
            font-family: 'Roboto', sans-serif;
        }
        div[data-testid="stMarkdownContainer"] strong {
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            font-size: 16px;
            color: #1F2937;
            line-height: 1.4;
        }
        div[data-testid="stMarkdownContainer"] em {
            font-family: 'Roboto', sans-serif;
            font-weight: 400;
            font-size: 14px;
            color: #6B7280;
            line-height: 1.5;
        }
        
        /* Button styling with deep blue accent */
        button[kind="primary"] {
            background-color: #1E40AF !important;
            font-family: 'Roboto', sans-serif;
            font-weight: 500;
            font-size: 14px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        button[kind="primary"]:hover {
            background-color: #1E3A8A !important;
            transform: scale(1.02);
        }
        button[kind="primary"]:focus {
            box-shadow: 0 0 0 3px #93C5FD;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Cover Image (top) - 3:4 aspect ratio
        if cover_image and os.path.isfile(cover_image):
            st.image(cover_image, use_column_width=True)
        else:
            # Fallback: gradient background with emoji icon (3:4 ratio)
            st.markdown(f"""
            <div style="width: 100%; aspect-ratio: 3/4; background: linear-gradient(135deg, {bg_color} 0%, {bg_color}DD 100%); 
                        display: flex; align-items: center; justify-content: center; font-size: 56px; 
                        border-radius: 8px; margin-bottom: 12px;">
                {icon}
            </div>
            """, unsafe_allow_html=True)
        
        # Title (bold, Roboto) - with "Title:" prefix
        st.markdown(f"**Title:** {title}", unsafe_allow_html=False)
        
        # Author (italic, Roboto) - with "Author:" prefix
        st.markdown(f"*Author: {author or 'Unknown Author'}*", unsafe_allow_html=False)
        
        # Open Button (primary action with deep blue)
        button_label = "▶ Open" if content_type in ["video", "movie", "audio"] else "📖 Open"
        if st.button(button_label, key=f"open_{item_id}", use_container_width=True, type="primary"):
            st.session_state[f"viewing_{item_id}"] = True
        
        # Show content viewer if Open button was clicked
        if st.session_state.get(f"viewing_{item_id}"):
            st.markdown("---")
            
            # Determine correct content source
            cursor = conn.cursor()
            cursor.execute(
                "SELECT source, path, url FROM content WHERE id = ?", 
                (item_id,)
            )
            result = cursor.fetchone()
            if result:
                source_type, file_path, file_url = result
                
                if content_type in ["video", "movie"]:
                    # Load video based on source type
                    if source_type == "youtube_link" and file_url:
                        st.video(convert_youtube_url(file_url))
                    elif source_type == "external_url" and file_url:
                        st.video(file_url)
                    elif source_type == "local_file" and file_path and os.path.isfile(file_path):
                        try:
                            with open(file_path, "rb") as f:
                                st.video(f.read())
                        except Exception as e:
                            st.error(f"Could not load video: {e}")
                    else:
                        st.warning(f"Video unavailable")
                
                elif content_type == "audio":
                    # Load audio based on source type
                    if source_type == "external_url" and file_url:
                        st.audio(file_url)
                    elif source_type == "local_file" and file_path and os.path.isfile(file_path):
                        try:
                            with open(file_path, "rb") as f:
                                st.audio(f.read())
                        except Exception as e:
                            st.error(f"Could not load audio: {e}")
                    else:
                        st.warning(f"Audio unavailable")
                
                elif content_type == "book" or content_type == "document":
                    # Display book/document information and download option
                    st.markdown(f"### 📖 {title}")
                    st.markdown(f"**Author:** {author or 'Unknown'}")
                    if description:
                        st.markdown(f"**Description:** {description}")
                    
                    if source_type == "external_url" and file_url:
                        st.markdown(f"[🔗 Open in new tab]({file_url})")
                    elif source_type == "local_file" and file_path and os.path.isfile(file_path):
                        try:
                            with open(file_path, "rb") as f:
                                file_ext = file_path.split('.')[-1] if '.' in file_path else 'pdf'
                                st.download_button(
                                    label=f"📥 Download {title}",
                                    data=f,
                                    file_name=f"{title}.{file_ext}",
                                    mime="application/pdf" if file_ext == 'pdf' else "application/octet-stream",
                                    key=f"view_dl_{item_id}"
                                )
                        except Exception as e:
                            st.error(f"Could not load file: {e}")
                    else:
                        st.info("File not available for viewing")
                
                # Close button
                if st.button("✖ Close", key=f"close_{item_id}"):
                    st.session_state[f"viewing_{item_id}"] = False
                    st.rerun()
