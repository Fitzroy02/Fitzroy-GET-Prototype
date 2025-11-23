---
name: Phase 2 - Cloud Sync + Upload/Search Enhancements
about: Implement cloud storage, enhanced upload interface, and role-based access control
title: '[PHASE-2] Cloud Sync + Upload/Search Enhancements'
labels: enhancement, phase-2, cloud-sync, upload
assignees: ''
---

## Phase 2: Cloud Sync + Upload/Search Enhancements

### Current Gaps

**Interface Issues:**
- ❌ No uploader on front face
- ❌ Drop-down does not toggle interface state
- ❌ Author role not included in system
- ❌ Search engine missing advanced features

**Backend Gaps:**
- ❌ No cloud storage integration
- ❌ No cross-device sync capability
- ❌ No user authentication system
- ❌ No encryption for sensitive content

### Implementation Checklist

#### 🔍 Search Engine Enhancements
- [ ] Add **search bar** with keyword search across all fields
- [ ] Implement **filters**:
  - [ ] Filter by role (Student/Practitioner/Author content)
  - [ ] Filter by content type (video/audio/book/document)
  - [ ] Filter by date uploaded (today/week/month/all time)
  - [ ] Filter by author name
- [ ] Add **sort options**:
  - [ ] Sort by relevance (default)
  - [ ] Sort by date (newest/oldest)
  - [ ] Sort by title (A-Z)
  - [ ] Sort by popularity (most viewed/downloaded)
- [ ] Implement **search suggestions** (autocomplete)
- [ ] Add **recent searches** history in session state
- [ ] Build **advanced search** with boolean operators (AND, OR, NOT)
- [ ] Ensure **search results populate playback slots dynamically**

#### 🎭 Role-Based Interface Toggle
- [ ] Implement **drop-down toggle** with three roles:
  - [ ] **Student** → playback only, no upload permissions
  - [ ] **Practitioner** → upload mode (video/audio/doc) + session management
  - [ ] **Author** → upload + attribution fields + curation tools
- [ ] Add **conditional rendering** based on selected role:
  - [ ] Hide upload UI for Student role
  - [ ] Show simplified upload for Practitioner
  - [ ] Show advanced upload with attribution for Author
- [ ] Implement **permission checks** before any upload action
- [ ] Add **role persistence** across sessions (store in session_state or DB)
- [ ] Create **role-switching animation/transition** for better UX

#### 📤 Uploader Components
- [ ] Add **uploader components** for multiple file types:
  - [ ] Video uploader (MP4, MOV, AVI) - max 500MB
  - [ ] Audio uploader (MP3, WAV, AAC) - max 100MB
  - [ ] Document uploader (PDF, DOCX, TXT) - max 50MB
- [ ] Implement **metadata capture** form:
  - [ ] Title (required, text input)
  - [ ] Author (required, auto-filled from user profile)
  - [ ] Role/Target audience (select: all/students/practitioners)
  - [ ] Tags (comma-separated, with suggestions)
  - [ ] Description (optional, text area)
  - [ ] Attribution fields for Authors:
    - [ ] Institution/Organization
    - [ ] License type (CC BY, CC BY-SA, All Rights Reserved)
    - [ ] Original publication date
    - [ ] DOI or reference link
- [ ] Add **file validation**:
  - [ ] Check file type matches expected format
  - [ ] Validate file size limits
  - [ ] Scan for malware/viruses (if possible)
  - [ ] Reject executable files (.exe, .sh, .bat)
- [ ] Implement **upload progress indicator**
- [ ] Add **preview after upload** (thumbnail, first page, audio waveform)
- [ ] Create **success/error notifications**

#### ☁️ Cloud Sync Layer
- [ ] Build **secure cloud sync layer** for cross-device continuity:
  - [ ] Choose cloud provider (Azure Blob Storage, AWS S3, or Google Cloud Storage)
  - [ ] Set up cloud storage buckets/containers
  - [ ] Configure access credentials securely (env variables)
- [ ] Implement **upload to cloud** functionality:
  - [ ] Upload local file to cloud storage
  - [ ] Generate secure cloud URL
  - [ ] Store cloud URL in database (instead of local path)
- [ ] Add **download from cloud** capability:
  - [ ] Generate temporary signed URLs for secure access
  - [ ] Implement streaming for large video files
  - [ ] Cache frequently accessed content locally
- [ ] Create **sync logic**:
  - [ ] Sync metadata across devices (SQLite → Cloud DB)
  - [ ] Sync viewing progress (watched/skipped status)
  - [ ] Sync user preferences and settings
  - [ ] Handle offline mode gracefully
- [ ] Implement **conflict resolution**:
  - [ ] Detect when same content modified on multiple devices
  - [ ] Use last-write-wins or manual merge strategy
  - [ ] Show sync status indicator (syncing/synced/conflict)

#### 🔐 Security & Encryption
- [ ] **Encrypt and store synced content privately**:
  - [ ] Encrypt files at rest (AES-256)
  - [ ] Encrypt files in transit (HTTPS/TLS)
  - [ ] Store encryption keys securely (Key Vault/Secrets Manager)
- [ ] Implement **user authentication**:
  - [ ] Add login/signup interface
  - [ ] Use OAuth 2.0 or similar (Google, Microsoft, GitHub)
  - [ ] Store user credentials securely (hashed passwords)
  - [ ] Implement session management (tokens, expiry)
- [ ] Add **authorization checks**:
  - [ ] Verify user identity before uploads
  - [ ] Check permissions before allowing downloads
  - [ ] Audit log for sensitive operations
- [ ] Implement **data privacy**:
  - [ ] User data isolation (each user sees only their content + shared)
  - [ ] Comply with GDPR/data retention policies
  - [ ] Add "Delete my data" functionality

#### 🎯 Role-Based Permissions
- [ ] **Validate role-based permissions**:
  - [ ] **Students**: consume content only
    - [ ] Can search all public content
    - [ ] Can view/download books, videos, documents
    - [ ] Can track their own progress
    - [ ] Cannot upload or modify content
  - [ ] **Practitioners**: upload + manage sessions
    - [ ] Can upload content for their students
    - [ ] Can create/manage homework assignments
    - [ ] Can view student progress
    - [ ] Can edit/delete their own uploads
  - [ ] **Authors**: curate library content
    - [ ] Can upload curated educational content
    - [ ] Can add rich attribution metadata
    - [ ] Can publish content to library catalog
    - [ ] Can edit/update their published content
- [ ] Create **permission matrix** in database:
  - [ ] Table: `user_permissions` (user_id, role, can_upload, can_edit, can_delete)
  - [ ] Function: `check_permission(user_id, action)` → boolean
- [ ] Add **permission denial messages**:
  - [ ] "You need Practitioner access to upload content"
  - [ ] "This content is restricted to students enrolled in this course"

#### 🔄 Feedback & Refinement
- [ ] **Integrate feedback loop for adaptive refinement**:
  - [ ] Add "Report issue" button on content items
  - [ ] Add content rating system (1-5 stars)
  - [ ] Add comment/review functionality
  - [ ] Collect user feedback on search relevance
  - [ ] Track upload success/failure rates
  - [ ] Monitor cloud sync performance metrics
- [ ] Implement **analytics dashboard**:
  - [ ] Most popular content
  - [ ] Search queries that return no results
  - [ ] Upload trends over time
  - [ ] User engagement metrics (time spent, completion rates)
- [ ] Build **A/B testing framework**:
  - [ ] Test different search algorithms
  - [ ] Test UI variations for upload flow
  - [ ] Test role switcher positions

### Database Schema Updates

```sql
-- Add cloud storage support
ALTER TABLE content ADD COLUMN storage_location TEXT DEFAULT 'local'; -- 'local' or 'cloud'
ALTER TABLE content ADD COLUMN cloud_url TEXT;
ALTER TABLE content ADD COLUMN encryption_key_id TEXT;

-- Add author attribution
ALTER TABLE content ADD COLUMN author TEXT;
ALTER TABLE content ADD COLUMN institution TEXT;
ALTER TABLE content ADD COLUMN license TEXT;
ALTER TABLE content ADD COLUMN doi TEXT;
ALTER TABLE content ADD COLUMN description TEXT;

-- Add user management
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL, -- 'student', 'practitioner', 'author', 'admin'
    created_at TEXT,
    last_login TEXT
);

-- Add permissions
CREATE TABLE IF NOT EXISTS user_permissions (
    user_id INTEGER,
    role TEXT,
    can_upload INTEGER DEFAULT 0,
    can_edit INTEGER DEFAULT 0,
    can_delete INTEGER DEFAULT 0,
    can_view_analytics INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add sync tracking
CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    device_id TEXT,
    sync_type TEXT, -- 'upload', 'download', 'metadata'
    content_id INTEGER,
    status TEXT, -- 'success', 'failed', 'pending'
    synced_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (content_id) REFERENCES content(id)
);

-- Add feedback
CREATE TABLE IF NOT EXISTS content_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id INTEGER,
    user_id INTEGER,
    rating INTEGER, -- 1-5
    comment TEXT,
    created_at TEXT,
    FOREIGN KEY (content_id) REFERENCES content(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### API Endpoints (Cloud Backend)

```python
# Required REST API endpoints for cloud sync

POST /api/auth/login
POST /api/auth/logout
POST /api/auth/signup

GET  /api/content/search?q={query}&type={type}&role={role}
POST /api/content/upload
GET  /api/content/{id}/download
PUT  /api/content/{id}/metadata
DELETE /api/content/{id}

GET  /api/user/profile
PUT  /api/user/profile
GET  /api/user/library
POST /api/user/sync

POST /api/feedback/submit
GET  /api/analytics/dashboard
```

### Testing Checklist

- [ ] Test Student role: cannot access upload UI
- [ ] Test Practitioner role: can upload video/audio/docs
- [ ] Test Author role: sees attribution fields
- [ ] Test search with all filter combinations
- [ ] Test cloud upload with 100MB+ file
- [ ] Test cloud download/streaming
- [ ] Test cross-device sync (upload on device A, view on device B)
- [ ] Test offline mode (graceful degradation)
- [ ] Test permission enforcement (unauthorized actions blocked)
- [ ] Test encryption (files encrypted at rest and in transit)
- [ ] Load test: 1000 content items in database
- [ ] Performance test: search response time < 500ms
- [ ] Security audit: penetration testing on auth/upload

### Milestone: Phase 2 Complete

**Success Criteria:**
- ✅ Upload interface functional for Practitioners and Authors
- ✅ Role-based interface toggle working correctly
- ✅ Advanced search with filters and sorting implemented
- ✅ Cloud storage integrated (upload/download working)
- ✅ Cross-device sync operational
- ✅ User authentication and authorization enforced
- ✅ Encryption enabled for sensitive content
- ✅ Feedback system collecting user input
- ✅ All tests passing
- ✅ Performance meets SLAs (<500ms search, <5s upload for 10MB)

**Deliverables:**
1. Updated `demo_app.py` with role-based UI and upload interface
2. New module: `upload_ui.py` for upload form and validation
3. New module: `cloud_sync.py` for cloud storage integration
4. New module: `auth.py` for user authentication
5. Updated database schema with new tables
6. API documentation for cloud backend
7. Testing report with all scenarios covered
8. Security audit report
9. User documentation for upload flow

**Next Steps:**
- Complete cloud sync implementation
- Validate stability with beta testers
- Gather feedback for refinement
- Prepare for Phase 3: Publisher Gateway

---

**Labels:** `enhancement`, `phase-2`, `cloud-sync`, `upload`, `authentication`, `security`  
**Milestone:** Phase 2 - Cloud Library (Persistent Mode)  
**Priority:** High  
**Estimated Effort:** 4-6 weeks  
**Dependencies:** Phase 1 completion, cloud provider account setup
