---
name: Visual Library Layout
about: Implement visual library layout with cover images and card-based display
title: '[Phase 1] Visual Library Layout Implementation'
labels: enhancement, phase-1, ui
assignees: ''
---

## Visual Library Layout - Implementation Checklist

### Overview
Implement a visually-rich library interface with cover images, card-based layout, and intuitive navigation for browsing content collections.

---

### Database Schema ✅
- [x] Add `cover_image` field to Library metadata schema
  - Field added to content table (14 fields total)
  - Migration script updated and executed
  - Demo content includes cover image paths

---

### Display Components ✅
- [x] Update display functions to render items in a grid of cards
  - Grid view: 3-column layout with card containers
  - List view: Horizontal cards with cover on left
  - Both views support cover images

- [x] Display cover image, title, author on each card
  - Grid view: 120px cover + title/author/metadata
  - List view: 100px cover + "Title: X, Author: Y" format
  - Color-coded by content type

- [x] Add fallback thumbnail generation if cover image missing
  - Gradient backgrounds with color coding
  - Emoji icons: 🎥 (video), 🎵 (audio), 📚 (book)
  - Base64 encoding for actual images

---

### User Experience Features
- [ ] Implement scrolling/pagination for large libraries
  - Add pagination controls (10/20/50 items per page)
  - Infinite scroll option
  - "Load More" button
  - Performance optimization for 100+ items

- [ ] Bind card click → load into correct loader
  - Click video card → open in video player
  - Click audio card → open in audio player
  - Click book card → open PDF viewer/download
  - Maintain playback state across navigation

---

### Testing & Quality Assurance
- [x] Test with mixed content (video, audio, book)
  - Demo content includes all three types
  - YouTube videos loading correctly
  - External URLs supported
  - Local file validation working

- [ ] Additional Testing Scenarios
  - Test with 50+ items in library
  - Test with missing cover images (fallback display)
  - Test with actual cover image files (PNG/JPG)
  - Test card click interactions
  - Test on mobile/tablet viewports
  - Test with long titles/author names
  - Test filter + sort combinations

---

### Technical Implementation Details

#### Current Schema (14 fields)
```sql
CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    user_role TEXT,
    type TEXT NOT NULL,
    source TEXT,
    path TEXT,
    url TEXT,
    tags TEXT,
    purchase_status TEXT,
    added_at TEXT,
    description TEXT,
    uploaded_by TEXT,
    cover_image TEXT  -- ✅ Added
)
```

#### Cover Image Display Logic
- **With cover_image**: Display actual PNG/JPG from `covers/` directory
- **Without cover_image**: Show color-coded gradient + emoji icon
- **Image encoding**: Base64 for inline HTML display
- **Helper function**: `get_image_base64(image_path)`

#### Current View Modes
1. **Grid View** (3-column cards)
   - 120px × 120px cover images
   - Title, author, type, date
   - Play/Read/Download actions

2. **List View** (horizontal cards)
   - 100px × 100px cover images
   - "Title: X, Author: Y" format
   - Expandable details section
   - Inline playback support

---

### Future Enhancements (Phase 2)
- [ ] Lazy loading for cover images
- [ ] Image caching and optimization
- [ ] Custom cover image upload
- [ ] Auto-generate thumbnails from video frames
- [ ] Drag-and-drop reordering
- [ ] Collection/playlist grouping
- [ ] Advanced filters (date range, purchase status)
- [ ] Search within library
- [ ] Bulk actions (delete, export, tag)

---

### Files Modified
- ✅ `demo_app.py` - Added cover_image field to schema and add_content()
- ✅ `library_view.py` - Updated display functions with cover image support
- ✅ `migrate_database.py` - Added cover_image column migration
- ✅ `covers/` - Created directory for storing thumbnails

---

### Dependencies
- Python packages: `streamlit`, `sqlite3`, `base64`
- Image formats: PNG, JPG/JPEG
- Browser compatibility: Base64 image display

---

### Acceptance Criteria
- [x] Cover images display correctly when files exist
- [x] Fallback thumbnails show when cover_image is missing
- [x] Grid and list views both support cover images
- [x] Title and author visible on all cards
- [ ] Pagination works smoothly for large libraries
- [ ] Card clicks trigger appropriate loaders
- [ ] Performance acceptable with 100+ items
- [ ] Mobile-responsive layout

---

### Related Issues
- [Phase 1] Upload & Search Flow (#issue-number)
- [Phase 1] Video Loading Improvements (#issue-number)
- [Phase 2] Cloud Sync & Storage (#issue-number)

---

### Notes
- Cover images stored in `covers/` directory
- Image paths relative to project root
- Base64 encoding handles inline display
- Fallback system prevents broken UI
- Color scheme: Video (#FF6B6B), Audio (#4ECDC4), Book (#95E1D3)
