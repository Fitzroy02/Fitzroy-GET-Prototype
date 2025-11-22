# 📜 Platform Policy

This document outlines the **security, privacy, and data retention policies** for the Practitioner–Student Collaboration Platform.  
It is intended for collaborators, stakeholders, and users to understand how the system protects data and ensures fairness.

---

## 🔐 Security Principles
- **Role-Based Access Control (RBAC)**  
  - Practitioners can create, assign, and review sessions and homework.  
  - Students can view, join, and submit homework, but cannot alter practitioner data.  
  - Roles are enforced at login and stored securely.

- **Session Privacy Settings**  
  - Practitioners decide whether sessions are *private*, *group-only*, or *public*.  
  - Recording permissions and share-link controls are configurable per session.  
  - Homework submissions are visible only to the practitioner who assigned them.

- **Audit & Transparency**  
  - Every action (session creation, homework submission, review, privacy update) is logged with timestamp and user ID.  
  - Practitioners and students can view their own logs for accountability.

---

## 🛡️ Privacy Measures
- **Homework Submissions**  
  - Stored securely in `uploads/homework/`.  
  - Accessible only to the practitioner and the submitting student.  
  - Feedback is private between practitioner and student.

- **Data Visibility**  
  - Students see only their own submissions and feedback.  
  - Practitioners see all submissions for their sessions.  
  - No cross-student visibility.

- **Transparency Dashboard**  
  - Students can view privacy settings applied to their sessions.  
  - Practitioners can configure privacy and retention policies.

---

## ⏳ Data Retention
- **Homework**: Deleted automatically after **30 days** (default).  
- **Audit Logs**: Retained for **90 days** (default).  
- **Session Archives**: Retained for **180 days** (default).  
- **Auto-Cleanup**: Enabled by default; practitioners can adjust retention values.

---

## ⚖️ Governance & Compliance
- All policies are designed to balance **learning collaboration** with **data protection**.  
- Practitioners are responsible for setting appropriate privacy and retention values.  
- Students are informed of retention timelines at the point of submission.  
- Logs and retention policies ensure compliance with ethical and civic standards.

---

## 📂 Versioning
This policy is version-controlled in GitHub.  
Changes must be reviewed and approved by stakeholders before merging into `main`.
