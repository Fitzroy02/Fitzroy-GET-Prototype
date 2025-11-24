import streamlit as st
from homework_ui import submit_homework
from storage import load_json, save_json
from upload_ui import upload_interface, update_content_schema
from library_view import library_view
from auth_ui import login_register_window, check_authentication, get_current_user, logout
import sqlite3
from datetime import datetime
import re
import os

def convert_youtube_url(url):
    """Convert YouTube watch URL to embed URL for better compatibility"""
    if "youtube.com/watch" in url:
        # Extract video ID from watch URL
        match = re.search(r'v=([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    elif "youtu.be/" in url:
        # Extract video ID from short URL
        match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
    return url

def load_video(path):
    """Load video from local file or URL with proper handling"""
    # Check if it's a URL
    if path.startswith("http://") or path.startswith("https://"):
        # Convert YouTube URLs to embed format
        return convert_youtube_url(path)
    
    # Try to load local file
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Video file not found: {path}")
        return None
    except Exception as e:
        st.warning(f"Could not load video file: {e}")
        return path  # Fallback to path

def init_onboarding_db():
    """Initialize onboarding video tracking database"""
    conn = sqlite3.connect("onboarding.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS viewed_flags (
        user TEXT,
        video_key TEXT,
        status TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    return conn, c

def init_content_db():
    """Initialize content index database with comprehensive schema"""
    conn = sqlite3.connect("content_index.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        user_role TEXT,
        type TEXT NOT NULL,
        source TEXT NOT NULL,
        path TEXT,
        url TEXT,
        tags TEXT,
        purchase_status TEXT,
        added_at TEXT NOT NULL,
        description TEXT,
        uploaded_by TEXT,
        cover_image TEXT
    )
    """)
    conn.commit()
    return conn, c

def main():
    # Check authentication first
    if not check_authentication():
        login_register_window()
        return
    
    # Get current user
    user = get_current_user()
    user_id = user['user_id']
    role = user['role']
    
    # Initialize video tracking database
    conn, cursor = init_onboarding_db()
    
    # Initialize content index database
    content_conn, content_cursor = init_content_db()
    
    # Update schema to support upload features
    update_content_schema()
    
    # Inject global CSS styles
    st.markdown(
        """
        <style>
        /* General font and colors */
        body {
            font-family: 'Open Sans', sans-serif;
            color: #333333;
            background-color: #F9FAFB;
        }

        /* Headings */
        h1, h2, h3 {
            color: #2E86AB; /* Primary accent blue */
            font-weight: 600;
        }

        /* Welcome banner */
        .welcome-banner {
            background-color: #e6f7ff;
            border: 2px solid #2E86AB;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }

        /* Footer */
        .footer {
            background-color: #fafafa;
            border-top: 2px solid #2E86AB;
            border-radius: 0 0 10px 10px;
            padding: 12px;
            margin-top: 40px;
            font-size: 13px;
            color: #555555;
            text-align: center;
        }

        /* Links */
        a {
            color: #2E86AB;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("🌟 Onboarding Demo")
    st.write("This demo shows how onboarding content can be embedded and tracked in the app.")
    
    # 📢 Admin notice
    st.warning("Admin note: The current videos, book, and scenarios are demo examples only. Replace with real onboarding content for production use.")

    # Welcome banner
    st.markdown(
        """
        <div class="welcome-banner">
        <h2>👋 Welcome!</h2>
        <p>Please enjoy these two short clips before you begin exploring the platform.<br>
        They set the tone for collaboration and explain how consent and retention work.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Videos - organized by source
    videos = [
        {"key": "whistling_youtube", "title": "🎶 Whistling Ad (YouTube)", "url": "https://www.youtube.com/watch?v=YTp7UQNE0Dw"},
        {"key": "intro_youtube", "title": "📺 Platform Introduction (YouTube)", "url": "https://www.youtube.com/watch?v=QYYvgFzR8Qc"},
        {"key": "github_video1", "title": "📚 Onboarding Part 1 (GitHub)", "url": "https://raw.githubusercontent.com/Fitzroy02/Fitzroy-GET-Prototype/main/media/onboarding_video1.mp4"},
        {"key": "github_video2", "title": "📚 Onboarding Part 2 (GitHub)", "url": "https://raw.githubusercontent.com/Fitzroy02/Fitzroy-GET-Prototype/main/media/onboarding_video2.mp4"}
    ]

    # Load sessions data
    sessions = load_json("sessions.json")
    
    # Display user info in sidebar
    st.sidebar.markdown("### 👤 User Profile")
    if user.get('is_guest'):
        st.sidebar.info(f"**Guest User**")
        st.sidebar.caption("Limited features available")
    else:
        st.sidebar.success(f"**{user_id}**")
        st.sidebar.caption(f"Role: {role.capitalize()}")
        if user.get('email'):
            st.sidebar.caption(f"📧 {user['email']}")
    
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    # Sidebar navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["🏠 Home", "📚 My Library", "🔍 Search", "📤 Upload (Practitioner)"],
        key="page_nav"
    )
    
    # Page routing based on sidebar navigation
    if page == "📚 My Library":
        library_view(user_id, role)
        conn.close()
        content_conn.close()
        return
    elif page == "📤 Upload (Practitioner)":
        if role != "practitioner":
            st.warning("⚠️ Switch to Practitioner role to access upload features")
        else:
            upload_interface(user_id, role)
        conn.close()
        content_conn.close()
        return
    elif page == "🔍 Search":
        st.markdown("---")
        # Jump to search section (handled below)
    # else: page == "🏠 Home" - continue with normal flow
    
    # Calculate and display video completion progress
    cursor.execute("SELECT video_key, status FROM viewed_flags WHERE user=?", (user_id,))
    records = cursor.fetchall()
    completed = {r[0] for r in records if r[1] == "viewed"}
    skipped = {r[0] for r in records if r[1] == "skipped"}
    
    progress = (len(completed) + len(skipped)) / len(videos) if len(videos) > 0 else 0
    
    st.subheader("📊 Video Onboarding Progress")
    st.progress(progress)
    st.write(f"Completion: {int(progress*100)}%")
    st.write(f"Viewed: {len(completed)}, Skipped: {len(skipped)}")
    st.markdown("---")
    
    # Single unified video player with selector
    st.subheader("🎬 Video Player")
    selected_video = st.selectbox(
        "Select a video to watch:",
        options=videos,
        format_func=lambda v: v["title"]
    )
    
    if selected_video:
        video_data = load_video(selected_video["url"])
        if video_data:
            st.video(video_data)
        
        col1, col2 = st.columns(2)
        if col1.button(f"Mark Viewed", key=f"{selected_video['key']}_viewed"):
            cursor.execute("INSERT INTO viewed_flags VALUES (?, ?, ?, ?)",
                          (user_id, selected_video["key"], "viewed", datetime.now().isoformat()))
            conn.commit()
            st.success(f"{selected_video['title']} marked as viewed!")
        
        if col2.button(f"Skip", key=f"{selected_video['key']}_skipped"):
            cursor.execute("INSERT INTO viewed_flags VALUES (?, ?, ?, ?)",
                          (user_id, selected_video["key"], "skipped", datetime.now().isoformat()))
            conn.commit()
            st.warning(f"{selected_video['title']} skipped.")
    
    st.info("End of demo content. In a real deployment, your own onboarding materials would appear here.")
    
    # Search functionality
    st.markdown("---")
    st.subheader("🔍 Search Content")
    
    # 🔖 Tag cloud - Browse by tags
    content_cursor.execute("SELECT tags FROM content")
    all_tags = content_cursor.fetchall()
    
    # Flatten and deduplicate
    tag_set = set()
    for row in all_tags:
        if row[0]:
            for t in row[0].split(","):
                tag_set.add(t.strip())
    
    selected_tag = None
    if tag_set:
        st.subheader("Browse by Tags")
        
        # 🎨 Define colours for tags (cycle through)
        colors = ["#ff4d4f", "#52c41a", "#1890ff", "#faad14", "#722ed1", "#13c2c2"]
        
        # Render tags as clickable buttons
        cols = st.columns(4)  # adjust layout
        for i, tag in enumerate(sorted(tag_set)):
            color = colors[i % len(colors)]
            if cols[i % 4].button(tag, key=f"tagcloud_{tag}"):
                selected_tag = tag
        
        st.markdown("---")
    
    def add_content(title, author, user_role, ctype, source, path_or_url, tags, purchase_status, cover_image=""):
        """Add new content metadata to the database with comprehensive fields."""
        # Determine path vs url based on source
        path = path_or_url if source == "local_file" else None
        url = path_or_url if source in ["youtube_link", "external_url"] else None
        
        content_cursor.execute("""
            INSERT INTO content 
            (title, author, user_role, type, source, path, url, tags, purchase_status, added_at, uploaded_by, cover_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, author, user_role, ctype, source, path, url, tags, purchase_status, 
              datetime.now().isoformat(), "system", cover_image))
        content_conn.commit()
    
    # Add demo content if database is empty
    content_cursor.execute("SELECT COUNT(*) FROM content")
    if content_cursor.fetchone()[0] == 0:
        # Use YouTube videos for demo content (no local files needed)
        add_content(
            "Whistling Ad Demo", 
            "Marketing Team", 
            "Practitioner", 
            "video", 
            "youtube_link",
            "https://www.youtube.com/embed/YTp7UQNE0Dw",
            "training, demo, introduction",
            "curated",
            "covers/whistling_ad.png"
        )
        add_content(
            "Platform Introduction",
            "John T. Hope",
            "Practitioner",
            "video",
            "youtube_link", 
            "https://www.youtube.com/embed/QYYvgFzR8Qc",
            "training, demo, tutorial",
            "curated",
            "covers/platform_intro.png"
        )
        add_content(
            "Getting Started Guide",
            "Documentation Team",
            "Author",
            "book",
            "external_url",
            "https://example.com/placeholder-guide.pdf",
            "documentation, guide",
            "curated",
            "covers/getting_started.png"
        )
    
    # 🔎 Search bar
    # Use session state to allow tag buttons to update the search
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    
    query = st.text_input("Search your books, videos, or movies:", value=st.session_state.search_query)
    
    # Update session state with current query
    if query != st.session_state.search_query:
        st.session_state.search_query = query
    
    # 📂 Filter dropdown
    filter_type = st.selectbox(
        "Filter by type:",
        ["all", "book", "video", "movie"]
    )
    
    # 🧮 Build query dynamically
    sql = "SELECT id, title, type, tags, path FROM content WHERE (title LIKE ? OR tags LIKE ?)"
    params = [f"%{query}%", f"%{query}%"]
    
    # If a tag was clicked, override query with that tag
    if selected_tag:
        sql = "SELECT id, title, type, tags, path FROM content WHERE tags LIKE ?"
        params = [f"%{selected_tag}%"]
    
    if filter_type != "all":
        sql += " AND type=?"
        params.append(filter_type)
    
    content_cursor.execute(sql, params)
    results = content_cursor.fetchall()
    
    # 📊 Display results
    if query or filter_type != "all":
        st.subheader("Search Results")
        if results:
            for item_id, title, ctype, tags, path in results:
                st.write(f"**{title}** ({ctype}) — tags: {tags}")
                
                # Show content
                if ctype == "book":
                    st.download_button("Download Book", data="(placeholder)", file_name=title+".pdf", key=f"download_{item_id}")
                elif ctype in ["video", "movie"]:
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
                
                # 🔖 Clickable tags
                tag_list = [t.strip() for t in tags.split(",")]
                tag_cols = st.columns(len(tag_list))
                for idx, t in enumerate(tag_list):
                    if tag_cols[idx].button(f"🏷️ {t}", key=f"tag_{item_id}_{t}"):
                        st.session_state.search_query = t
                        st.rerun()
                
                st.markdown("---")
        else:
            st.warning("No matches found.")

    # Role-based dashboard shortcuts
    st.markdown("---")
    st.header("Quick Actions")
    
    if role == "student":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📚 **My Library**\nAccess your purchased content")
        with col2:
            st.info("🔍 **Search**\nDiscover new content")
        with col3:
            st.info("📝 **Homework**\nSubmit assignments")
        
        # Homework submission for a given session
        if sessions:
            session_id = st.selectbox("Choose session for homework", list(sessions.keys()))
            if session_id:
                submit_homework(session_id, user_id)

    elif role == "practitioner":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📤 Upload Content", use_container_width=True):
                st.info("Navigate to **📤 Upload (Practitioner)** page")
        with col2:
            if st.button("📚 Manage Library", use_container_width=True):
                st.info("Navigate to **📚 My Library** page")
        with col3:
            if st.button("🔍 Browse Content", use_container_width=True):
                st.info("Navigate to **🔍 Search** page")
        
        st.markdown("---")
        st.subheader("Session Management")
        # Example: create a new session
        new_title = st.text_input("New session title")
        if st.button("Create Session"):
            sessions[new_title] = {
                "title": new_title,
                "type": "group",
                "participants": [],
                "homework": {"tasks": []},
            }
            save_json("sessions.json", sessions)
            st.success(f"Session '{new_title}' created!")

    # Footer
    st.markdown(
        """
        <div class="footer">
        📜 Consent Reminder: By using this platform, you agree to the 
        <a href='./STUDENT_INFO.md'>Student & Patient Information</a>.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Close database connections
    conn.close()
    content_conn.close()

if __name__ == "__main__":
    main()
