import streamlit as st
from homework_ui import submit_homework
from storage import load_json, save_json

def main():
    st.title("🎓 Practitioner–Student Collaboration Platform")

    # Intro video
    st.markdown(
        """
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/QYYvgFzR8Qc"
        frameborder="0" allowfullscreen></iframe>
        """,
        unsafe_allow_html=True
    )

    # Load sessions data
    sessions = load_json("sessions.json")

    # Simple role selector for demo purposes
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

    # Footer message for transparency
    st.markdown(
        """
        <div style="
            background-color:#fafafa;
            border-top:1px solid #dddddd;
            padding:10px;
            margin-top:30px;
            font-size:12px;
            color:#555;
        ">
        📜 Consent Reminder: By using this platform, you agree to the 
        <a href='./STUDENT_INFO.md'>Student & Patient Information</a>.
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
