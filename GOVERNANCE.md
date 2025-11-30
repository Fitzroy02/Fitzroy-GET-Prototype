# ⚖️ Governance Workflow Guide

This document explains how governance checks are enforced in this repository.

---

## 📂 CODEOWNERS
- Located at `.github/CODEOWNERS`.
- Defines which stakeholders must review changes to specific files.
- Example:
  ```
  POLICY.md @<privacy-officer> @<practitioner-lead>
  homework_ui.py @<practitioner-lead>
  ```
- GitHub automatically assigns these reviewers when a PR touches the listed files.
- **Result:** Governance files cannot be merged without stakeholder approval.

---

## 📝 Pull Request Template
- Located at `.github/pull_request_template.md`.
- Auto-populates every new PR with:
  - Summary and rationale sections
  - Governance checklist table
  - Reviewer assignment placeholders
- Example checklist items:
  - RBAC definitions unchanged
  - Session privacy enforced
  - Retention policies correct (30d/90d/180d)
  - Consent banner aligned with POLICY.md
  - README links to POLICY.md
  - CODEOWNERS enforced

---

## 🔄 How They Work Together
1. **Contributor opens a PR** → Template appears with governance checklist.
2. **Contributor fills in summary/rationale** → Reviewers see context.
3. **GitHub auto-assigns reviewers** via CODEOWNERS.
4. **Reviewers validate checklist items** before approving.
5. **Merge blocked** until required reviewers approve.

---

## ✅ Best Practices
- Always update the checklist when governance files change.
- Do not bypass CODEOWNERS — approvals are mandatory.
- Keep POLICY.md as the single source of truth for privacy and retention.
- Use clear commit messages (e.g. `"Add POLICY.md and consent banner"`).
- Treat governance review as a civic responsibility, not just a technical step.

---

## 🎯 Goals
- Ensure **transparency** in policy changes.
- Maintain **auditability** through structured reviews.
- Protect **student privacy** through mandatory checks.
- Balance **collaboration** with **data protection** under civic/ethical standards.
