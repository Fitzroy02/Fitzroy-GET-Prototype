import streamlit as st
from homework_ui import submit_homework
from storage import load_json, save_json

def main():
    st.title("🎓 Practitioner–Student Collaboration Platform")

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

if __name__ == "__main__":
    main()
