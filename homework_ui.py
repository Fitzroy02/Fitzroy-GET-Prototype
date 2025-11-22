import streamlit as st
from datetime import datetime
import storage  # type: ignore
from storage import save_json, load_json

def submit_homework(session_id, student_id):
    st.header("📚 Homework Submission")

    # Consent banner
    st.markdown(
        """
        ### 📜 Consent Notice
        By submitting your homework, you agree to the [Student & Patient Information](./STUDENT_INFO.md).

        - Your submission is private between you and your practitioner/teacher.
        - Homework files are retained for **30 days** and then deleted automatically.
        - Feedback is stored securely and visible only to you.
        - Audit logs are retained for **90 days**; session archives for **180 days**.
        - You have the right to ask questions about privacy and retention at any time.
        """
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
