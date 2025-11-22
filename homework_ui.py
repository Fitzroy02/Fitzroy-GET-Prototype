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
        By submitting your homework, you consent to storage and review under the 
        [Platform Policy](./POLICY.md).  
        - Submissions are private between you and your practitioner.  
        - Files will be retained for **30 days** and then deleted automatically.  
        - Feedback will be stored securely and visible only to you.  
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
