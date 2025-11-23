import streamlit as st
from homework_ui import submit_homework
from storage import load_json, save_json

def main():
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
    
    st.title("🎓 Practitioner–Student Collaboration Platform")

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

    # Videos
    st.subheader("🎶 Whistling Ad")
    st.video("https://www.youtube.com/watch?v=YTp7UQNE0Dw")

    st.subheader("📺 Platform Introduction")
    st.video("https://www.youtube.com/watch?v=QYYvgFzR8Qc")

    # Load sessions data
    sessions = load_json("sessions.json")

    # Role selector follows after welcome videos
    role = st.sidebar.selectbox("Select role", ["student", "practitioner"])
    user_id = st.sidebar.text_input("User ID", "user-001")

    if role == "student":
        st.header("Student Dashboard")
        # Example: show homework submission for a given session
        session_id = st.selectbox("Choose session", list(sessions.keys()))
        if session_id:
            submit_homework(session_id, user_id)

    elif role == "practitioner":
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

if __name__ == "__main__":
    main()
