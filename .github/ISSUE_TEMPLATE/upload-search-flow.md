---
name: Add Upload + Search Flow to Hub Interface
about: Implement role-based upload functionality and search engine layer
title: '[FEATURE] Add Upload + Search Flow to Hub Interface'
labels: enhancement, phase-1
assignees: ''
---

## Current State

- ✅ Front face shows video onboarding screens (2 YouTube videos)
- ✅ Audio/video playback functionality exists
- ✅ Drop-down switches roles (Student/Practitioner) in sidebar
- ❌ No uploader present for content submission
- ❌ Role drop-down doesn't change interface state/permissions
- ❌ Search engine layer not yet implemented
- ✅ SQLite content index exists (`content_index.db`)
- ✅ Tag cloud browsing implemented

## Proposed Adjustments

### 1. Role-Based Interface Toggle

Drop-down should dynamically change the interface based on selected role:

- **Student Role:**
  - Playback-only mode
  - Search and browse content
  - Track viewing progress (viewed/skipped)
  - No upload permissions

- **Practitioner Role:**
  - Upload mode enabled
  - Upload: video, audio, documents (PDF, DOCX)
  - Set homework assignments
  - Manage sessions
  - View student progress

- **Author Role (Future):**
  - Upload curated content
  - Add attribution fields (author name, institution, license)
  - Tag content for discoverability
  - Publish to library

### 2. Upload Interface

**Required Fields:**
```python
- Title (text input)
- Content Type (select: video, audio, book, document)
- File Upload (file_uploader)
- Tags (comma-separated text input)
- Description (text area)
- Author/Creator (auto-filled from user profile)
- Role/Permission (who can access: all, students, practitioners)
```

**Database Schema Update:**
```sql
ALTER TABLE content ADD COLUMN author TEXT;
ALTER TABLE content ADD COLUMN description TEXT;
ALTER TABLE content ADD COLUMN permissions TEXT;
ALTER TABLE content ADD COLUMN uploaded_by TEXT;
```

### 3. Search Engine Enhancement

**Current:** Basic search by title and tags
**Needed:**
- Filter by role (Student/Practitioner/Author content)
- Filter by content type (book, video, movie, audio, document)
- Filter by date uploaded
- Filter by author
- Sort options (relevance, date, popularity)
- Search results pagination

### 4. Dynamic Content Display

Results should populate playback/download slots dynamically:
- Video/Audio → `st.video()` or `st.audio()` player
- Books/Documents → `st.download_button()`
- Show metadata (author, date, tags)
- Track interactions (views, downloads)

## Implementation Checklist

### Phase 1: Role-Based UI Toggle
- [ ] Add role state management in `st.session_state`
- [ ] Create conditional UI rendering based on role
- [ ] Hide/show upload section for Student vs Practitioner
- [ ] Add permission checks before rendering upload UI
- [ ] Test role switching preserves search state

### Phase 2: Upload Interface
- [ ] Create `upload_content()` function in new `upload_ui.py` module
- [ ] Add file uploader with type validation (video, audio, PDF, DOCX)
- [ ] Implement metadata form (title, tags, description)
- [ ] Add author attribution (from user profile or manual input)
- [ ] Save uploaded files to designated storage path
- [ ] Insert metadata into `content_index.db`
- [ ] Show success confirmation with preview
- [ ] Add error handling for invalid files/large files
- [ ] Implement file size limits (e.g., 100MB for videos)

### Phase 3: Enhanced Search Engine
- [ ] Add advanced filter UI (role, type, date range, author)
- [ ] Update SQL queries to support multiple filter combinations
- [ ] Add sort dropdown (relevance, date, title, author)
- [ ] Implement pagination (show 10 results per page)
- [ ] Add "No results" state with suggestions
- [ ] Add search history (recent searches in session state)
- [ ] Add "Clear filters" button
- [ ] Test search performance with 100+ items

### Phase 4: Dynamic Content Display
- [ ] Refactor results display to handle mixed content types
- [ ] Add audio player support (`st.audio()`)
- [ ] Add document preview (PDF viewer or download)
- [ ] Show rich metadata cards (author, date, description, tags)
- [ ] Add view/download tracking to database
- [ ] Add "Add to Favorites" functionality
- [ ] Show related content suggestions
- [ ] Add content rating/feedback system

### Phase 5: Database & Storage
- [ ] Update `content` table schema with new columns
- [ ] Create `uploads/` directory structure (videos/, audio/, books/, docs/)
- [ ] Implement file naming convention (timestamp + sanitized title)
- [ ] Add database migration script for schema changes
- [ ] Test database queries with new columns
- [ ] Add indexes for performance (author, type, added_at)

### Phase 6: Testing & Validation
- [ ] Test upload as Student (should fail/hide)
- [ ] Test upload as Practitioner (should succeed)
- [ ] Test search with various filter combinations
- [ ] Test file upload with edge cases (special chars, large files)
- [ ] Test database integrity after uploads
- [ ] Performance test with 100+ content items
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile responsiveness check

## User Journey Examples

### Journey 1: Student Searches Content
1. Student logs in → role set to "Student"
2. Interface shows: search bar + tag cloud + recent content
3. Student searches "ethics" → filters by tag
4. Results show: "Philosophy of AI" book + related videos
5. Student clicks video → plays inline
6. Progress tracked: "viewed" status saved to database
7. Student downloads book → download count incremented

### Journey 2: Practitioner Uploads Homework Video
1. Practitioner logs in → role set to "Practitioner"
2. Interface shows: upload section + content management
3. Practitioner clicks "Upload Content"
4. Fills form:
   - Title: "Week 3 Homework Instructions"
   - Type: Video
   - Tags: homework, week3, instructions
   - File: uploads video (50MB)
5. Submits → file saved to `uploads/videos/`
6. Metadata inserted into database with author info
7. Success message: "Content uploaded and searchable"
8. Students can now find it via search

### Journey 3: Author Curates Library Content
1. Author logs in → role set to "Author"
2. Interface shows: advanced upload with attribution
3. Author uploads curated content:
   - Title: "Introduction to Ethics in AI"
   - Type: Book (PDF)
   - Author: "Dr. Jane Smith"
   - Institution: "University of Example"
   - License: "Creative Commons BY-SA"
4. Tags: ethics, ai, philosophy, textbook
5. Submits → content published to library
6. All roles can now search and access this content

## Technical Notes

### File Storage Paths
```
/workspaces/Fitzroy-GET-Prototype/
├── uploads/
│   ├── videos/
│   ├── audio/
│   ├── books/
│   └── documents/
├── content_index.db
└── onboarding.db
```

### Metadata Schema
```python
{
    "id": 1,
    "title": "Ethics in AI",
    "type": "book",
    "tags": "ethics, ai, philosophy",
    "path": "/uploads/books/20251123_ethics_in_ai.pdf",
    "added_at": "2025-11-23T10:30:00",
    "author": "Dr. Jane Smith",
    "description": "Comprehensive guide to ethical considerations...",
    "permissions": "all",  # all, students, practitioners, authors
    "uploaded_by": "user-001",
    "downloads": 0,
    "views": 0
}
```

### Permission Matrix
| Role | Search | View | Download | Upload | Edit Own | Delete Own |
|------|--------|------|----------|--------|----------|------------|
| Student | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Practitioner | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Author | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ (all) |

## Dependencies

- `streamlit >= 1.28.0` (file uploader, session state)
- `sqlite3` (database)
- `python-magic` or `mimetypes` (file type validation)
- `pathlib` (file path handling)
- `datetime` (timestamps)

## Acceptance Criteria

- [ ] Students cannot see upload UI
- [ ] Practitioners can upload and manage their own content
- [ ] Search filters work correctly with all combinations
- [ ] Uploaded files are saved with correct paths
- [ ] Metadata is searchable immediately after upload
- [ ] File type validation prevents invalid uploads
- [ ] Large files (>100MB) show appropriate error message
- [ ] All user journeys tested successfully
- [ ] No database errors or orphaned files
- [ ] Performance remains acceptable with 100+ items

## Related Issues

- #XX: Implement cloud storage (Phase 2)
- #XX: Add user authentication system
- #XX: Publisher gateway (Phase 3)

## References

- Current implementation: `demo_app.py`
- Database schema: `content_index.db`
- Policy framework: `POLICY.md`, `GOVERNANCE.md`
- User documentation: `STUDENT_INFO.md`

---

**Labels:** `enhancement`, `phase-1`, `upload`, `search`, `role-based-access`  
**Milestone:** Phase 1 - Customer Library (Local Mode)  
**Priority:** High
