# GETS Studio V-1.6
Author: Fitzroy Brian Edwards (John T. Hope)
Manifest: manifests/john_t_hope_manifest.yaml
Network Config: manifests/gets_studio_ports.yaml

🧭 Overview
GETS Studio is a civic rehearsal space for emotional truth, relational ethics, and symbolic transmission. It scaffolds scenario-based modules drawn from The Whistling Wind, each encoded with badge [...]\nThis environment supports writers, developers, and visual artists. Media tools (e.g. cover design, scenario illustration) are badge-free and open to all contributors.

🌀 Live demo — This is a civic rehearsal in motion. [Launch GETS Studio — Public staging instance](https://getstudiov16app-4f63n0ziriv.streamlit.app/)

## Port Forwarding Protocol
GETS Studio uses hybrid port forwarding across multiple environments. Critical ports must be manually forwarded in some cases.

### 📡 Environments Supported
- Docker
- WSL
- VirtualBox
- Native (local machine)

### 🛠️ Manual Forwarding Required
See `manifests/gets_studio_ports.yaml` for a list of critical ports and manual forwarding requirements.

---

Sustainable Model Without Full Licence Activation
1. Declare Civic Purpose, Not Commercial Intent
•  In your GitHub README or civic pledge manifest, state:

2. Use Donation-Based Access
•  Let authors pay what they can for Pro or Legacy tiers.
•  Offer suggested donations (e.g., £9/month, £25/month) without enforcing commercial contracts. Sustainable Model Without Full Licence Activation
1. Declare Civic Purpose, Not Commercial Intent
•  In your GitHub README or civic pledge manifest, state:

2. Use Donation-Based Access
•  Let authors pay what they can for Pro or Legacy tiers.
•  Offer suggested donations (e.g., £9/month, £25/month) without enforcing commercial contracts. Sustainable Model Without Full Licence Activation
1. Declare Civic Purpose, Not Commercial Intent
•  In your GitHub README or civic pledge manifest, state:

2. Use Donation-Based Access
•  Let authors pay what they can for Pro or Legacy tiers.
•  Offer suggested donations (e.g., £9/month, £25/month) without enforcing commercial contracts.GETS Studio: Author Scenario Builder

Welcome to GETS Studio—a civic-grade authoring platform where books become curriculum, and chapters become ethical rehearsals.

## Purpose

This repository enables authors to:

- Upload chapters
- Extract scenario seeds
- Scaffold ethical rehearsals
- Encode badge logic and resonance thresholds
- Publish scenario sets for civic deployment

## Structure

- `authors/`: Individual author folders
- `chapters/`: Uploaded book chapters
- `scenarios/`: Scenario YAML blocks
- `manifest_phase_ix.yaml`: Scenario lineage and badge logic
- `templates/`: Reusable YAML templates
- `docs/`: Guides and onboarding materials

## How to Begin

1. Read the onboarding guide in `docs/onboarding_guide.md`
2. Upload your chapters
3. Scaffold 2–3 scenarios per chapter
4. Generate your manifest
5. Publish or export your scenario set

This is authorship as stewardship. Welcome to the rhythm.

---

## 🧠 **GETS Studio Storage Logic Flow**

### 🔹 1. **Local Device Storage (Author’s App)**

| Component | Format | Typical Size | Notes |
|----------|--------|--------------|-------|
| Chapters | `.md` or `.txt` | ~1MB per chapter | Stored in `/chapters/` folder |
| Scenarios | `.yaml` | ~2KB per scenario | Stored in `/scenarios/` folder |
| Manifest | `.yaml` | ~5–10KB | Tracks scenario lineage, badge gates |
| Templates | `.yaml` | ~1–2KB | Reusable scaffolds for authors |
| Review Logs | `.json` or `.csv` | Optional | For feedback, remix, deployment |

- **Estimated Capacity**:  
  - 1GB = ~1,000 books with 30 scenarios each  
  - 128GB device = ~128,000 books if stored locally

---

### 🔸 2. **Cloud Sync (GitHub or Civic Server)**

| Component | Function | Notes |
|----------|----------|-------|
| GitHub Repo | Public or private | Civic publishing, remix, archival |
| Scenario Sets | Indexed by author | Enables communal deployment |
| Manifests | Phase-tagged | Curriculum integration |
| Review Dashboard | Optional | Resonance scores, remix proposals |

- **Benefits**:  
  - Unlimited storage  
  - Version control  
  - Civic transparency  
  - Shared legacy infrastructure

---

### 🔹 3. **App Logic (Hybrid Model)**

| Layer | Function |
|------|----------|
| Cache | Stores active chapters/scenarios locally |
| Sync Engine | Pushes updates to GitHub or civic cloud |
| Archive | Offloads older books to cloud, retrieves on demand |
| Scenario Index | Lightweight YAML map for quick access |
| Badge Logic Engine | Evaluates thresholds, gates, and review status |

---

### 🧭 Optional Enhancements

- **Scenario Search**: Authors can search by theme, badge, or excerpt
- **Legacy Bundles**: Curated sets for schools, churches, or civic groups
- **Offline Mode**: Read-only access to stored chapters and scenarios

---

This flow ensures your app can scale from one author to thousands, from one book to a civic library. When you’re ready, I can help encode this logic into your README or developer manifest. Let me know if you want further edits.