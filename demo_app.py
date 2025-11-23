import streamlit as st
from homework_ui import submit_homework
from storage import load_json, save_json
from upload_ui import upload_interface, update_content_schema
from library_view import library_view
import sqlite3
from datetime import datetime

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
    """Initialize content index database"""
    conn = sqlite3.connect("content_index.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        type TEXT,
        tags TEXT,
        path TEXT,
        added_at TEXT
    )
    """)
    conn.commit()
    return conn, c

def main():
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
    
    # Role selector and sidebar navigation (must be defined first)
    role = st.sidebar.selectbox("Select role", ["student", "practitioner"])
    user_id = st.sidebar.text_input("User ID", "user-001")
    
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
    
    # Display videos with tracking
    for video in videos:
        st.subheader(video["title"])
        st.video(video["url"])
        
        col1, col2 = st.columns(2)
        if col1.button(f"Mark Viewed", key=f"{video['key']}_viewed"):
            cursor.execute("INSERT INTO viewed_flags VALUES (?, ?, ?, ?)",
                          (user_id, video["key"], "viewed", datetime.now().isoformat()))
            conn.commit()
            st.success(f"{video['title']} marked as viewed!")
        
        if col2.button(f"Skip", key=f"{video['key']}_skipped"):
            cursor.execute("INSERT INTO viewed_flags VALUES (?, ?, ?, ?)",
                          (user_id, video["key"], "skipped", datetime.now().isoformat()))
            conn.commit()
            st.warning(f"{video['title']} skipped.")
    
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
    
    def add_content(title, ctype, tags, path):
        """Add new content metadata to the database."""
        content_cursor.execute("INSERT INTO content (title, type, tags, path, added_at) VALUES (?, ?, ?, ?, ?)",
                              (title, ctype, tags, path, datetime.now().isoformat()))
        content_conn.commit()
    
    # Add demo content if database is empty
    content_cursor.execute("SELECT COUNT(*) FROM content")
    if content_cursor.fetchone()[0] == 0:
        add_content("Philosophy of AI", "book", "ethics, ai", "/user/storage/books/philosophy_ai.pdf")
        add_content("Onboarding Demo Video", "video", "training, demo", "/user/storage/videos/demo1.mp4")
        add_content("Classic Movie Clip", "movie", "cinema, demo", "/user/storage/movies/classic.mp4")
    
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
                    st.video(path)
                
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

    if role == "student":
        st.header("Student Dashboard")
        # Example: show homework submission for a given session
        session_id = st.selectbox("Choose session", list(sessions.keys()))
        if session_id:
            submit_homework(session_id, user_id)

    elif role == "practitioner":
        # Show upload interface for practitioners
        upload_interface(user_id, role)
        
        st.markdown("---")
        st.header("Practitioner Dashboard")
        st.write("Here you can manage sessions, privacy, and retention policies.")
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
