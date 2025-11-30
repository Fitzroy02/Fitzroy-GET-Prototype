import streamlit as st
from datetime import datetime
import storage  # type: ignore
from storage import save_json, load_json

def submit_homework(session_id, student_id):
    st.header("📚 Homework Submission")

    # Consent banner
    st.markdown(
        """
        <div style="
            background-color:#f0f8ff;
            border:1px solid #cccccc;
            border-radius:8px;
            padding:15px;
            margin-top:10px;
            margin-bottom:20px;
        ">
        <h3>📜 Consent Notice</h3>
        <p>By submitting your homework, you agree to the 
        <a href='./STUDENT_INFO.md'>Student & Patient Information</a>.</p>
        <ul>
          <li>Private between you and your practitioner/teacher</li>
          <li>Retained for <b>30 days</b>, then deleted</li>
          <li>Feedback stored securely, visible only to you</li>
          <li>Audit logs kept for <b>90 days</b>; session archives for <b>180 days</b></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    sessions = load_json("sessions.json")
    session = sessions.get(session_id)
    if not session:
        st.error("Session not found.")
        return

    tasks = session.get("homework", {}).get("tasks", [])
    if not tasks:
        st.info("No homework tasks assigned.")
        return

    for task in tasks:
        st.subheader(task["description"])
        st.write(f"Due: {task['due_date']} | Status: {task['status']}")

        uploaded_file = st.file_uploader(
            f"Upload submission for {task['id']}", type=["pdf", "docx", "txt"]
        )
        notes = st.text_area("Notes (optional)", key=f"notes-{task['id']}")

        if uploaded_file and st.button(f"Submit {task['id']}"):
            filename = f"uploads/homework/{student_id}-{task['id']}-{uploaded_file.name}"
            with open(filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            submission = {
                "student_id": student_id,
                "submitted_at": datetime.utcnow().isoformat(),
                "file_path": filename,
                "notes": notes
            }

            task.setdefault("submissions", []).append(submission)
            task["status"] = "submitted"

            save_json("sessions.json", sessions)
            st.success(f"Homework {task['id']} submitted successfully!")
