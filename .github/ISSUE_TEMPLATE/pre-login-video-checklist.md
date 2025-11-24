---
name: Pre-Login Video Loading Checklist
about: Ensure video loading works correctly before user authentication
title: "[Pre-Login] Video Loading Requirements"
labels: enhancement, bug fix, testing
assignees: ''
---

## Pre-Login Video Loading Requirements

This checklist ensures video and audio content loads properly throughout the app, with proper detection, path handling, and error management.

---

## ✅ Detection Logic Implementation

### Replace Hard-Coded Checks
- [x] Replace `if "youtube.com" in path` with unified detection function
- [x] Create `convert_youtube_url()` helper function
- [x] Detect YouTube watch URLs: `youtube.com/watch?v=VIDEO_ID`
- [x] Detect YouTube short URLs: `youtu.be/VIDEO_ID`
- [x] Extract video ID using split/regex pattern
- [x] Convert to embed format: `youtube.com/embed/VIDEO_ID`
- [x] Handle already-embedded URLs (pass through unchanged)

### Local File Detection
- [x] Use `os.path.isfile(path)` to verify file existence and type
- [x] Distinguish between files and directories
- [x] Check file accessibility before opening
- [x] Handle permission errors gracefully

### URL Detection
- [x] Check for `http://` and `https://` prefixes
- [x] Handle generic URLs (non-YouTube remote content)
- [x] Pass through remote URLs directly to `st.video()`/`st.audio()`

---

## 📂 File Path Validation

### Path Type Verification
- [ ] Verify all local file paths use absolute paths (e.g., `/workspaces/...`)
- [ ] OR verify paths are relative to app root (`uploads/videos/file.mp4`)
- [x] Document path conventions in code comments
- [ ] Test path resolution from different working directories

### Upload Directory Structure
- [ ] Ensure `uploads/videos/` directory exists
- [ ] Ensure `uploads/audios/` directory exists
- [ ] Ensure `uploads/books/` directory exists
- [ ] Create directories automatically if missing
- [ ] Set proper permissions (read/write for app, read-only for users)

### Demo Content Paths
- [x] Replace `/user/storage/` paths with working alternatives
- [x] Use YouTube URLs for demo videos (no local files needed)
- [x] Use placeholder URLs for demo books
- [ ] Document where demo content should be placed in production

---

## 🎬 YouTube URL Handling

### Embed URL Storage
- [x] Store YouTube URLs in embed format in database
- [ ] Add migration script to convert existing watch URLs to embed format
- [ ] Update upload interface to convert YouTube URLs on save
- [ ] Validate embed URLs before storage
- [ ] Document embed URL format in schema comments

### Database Schema
- [ ] Add `storage_type` column: `local`, `youtube`, `url`
- [ ] Add `original_url` column to preserve watch URLs if needed
- [ ] Update `add_content()` function to set storage_type
- [ ] Create database migration script
- [ ] Update all queries to handle storage_type field

### URL Conversion Testing
- [x] Test `youtube.com/watch?v=VIDEO_ID` → `youtube.com/embed/VIDEO_ID`
- [x] Test `youtu.be/VIDEO_ID` → `youtube.com/embed/VIDEO_ID`
- [x] Test already-embedded URLs (should pass through)
- [ ] Test with query parameters: `watch?v=ID&t=30s`
- [ ] Test with playlist URLs
- [ ] Test with timestamp URLs: `youtu.be/ID?t=30`

---

## 🛡️ Error Handling & Fallback

### Error Cases Covered
- [x] FileNotFoundError: Show `st.error()` with specific message
- [x] Permission errors: Show `st.error()` with exception details
- [x] Invalid paths: Show `st.warning()` with path details
- [x] Network errors for URLs: Graceful fallback message
- [x] Corrupted files: Show error message instead of crash

### Fallback Messages
- [x] Video unavailable: `"Video unavailable. Path not found: {path}"`
- [x] Audio unavailable: `"Audio unavailable. Path not found: {path}"`
- [x] File read error: `"Could not open video file: {exception}"`
- [ ] Network timeout: `"Could not load video. Check network connection."`
- [ ] Invalid format: `"Unsupported video format. Please upload MP4, MOV, or AVI."`

### User Experience
- [x] No app crashes from missing files
- [x] Clear, actionable error messages
- [x] Path shown in error for debugging
- [ ] Retry button for network failures
- [ ] Contact support link in persistent errors

---

## 🧪 Testing Requirements

### Test with Local MP4 Files
- [ ] Create test video: `uploads/videos/test.mp4`
- [ ] Upload via Upload interface (Practitioner role)
- [ ] Verify file saves to correct directory
- [ ] View in Library - test inline playback
- [ ] Search for video - test preview display
- [ ] Download video - verify file integrity
- [ ] Remove video - verify file deletion

### Test with YouTube Links
- [x] Add YouTube watch URL to database
- [x] Verify automatic conversion to embed format
- [x] Test playback in Library grid view
- [x] Test playback in Library list view
- [x] Test preview in Search results
- [x] Test in Home page video selector
- [ ] Test with restricted videos (age-restricted, region-locked)
- [ ] Test with private/unlisted videos

### Test Error Scenarios
- [x] Missing file path in database
- [x] File path points to non-existent file
- [ ] File path points to directory instead of file
- [ ] Network disconnected (YouTube video)
- [ ] Invalid YouTube URL format
- [ ] Corrupted video file
- [ ] Insufficient permissions to read file

### Cross-Page Testing
- [x] Home page: Video selector dropdown
- [x] Library: Grid view playback
- [x] Library: List view playback
- [x] Search: Results preview
- [ ] Upload: Preview before save
- [ ] Upload: Validation on submit

---

## 📝 Code Quality & Documentation

### Code Organization
- [x] Create helper functions: `convert_youtube_url()`, `load_video()`, `load_audio()`
- [x] Remove duplicate code across pages
- [x] Use consistent error handling patterns
- [x] Add docstrings to all helper functions
- [ ] Add type hints to function parameters
- [ ] Create unit tests for helper functions

### Documentation Updates
- [ ] Update ARCHITECTURE.md with video loading flow
- [ ] Document three-case logic: YouTube / Local / Fallback
- [ ] Add troubleshooting section for common errors
- [ ] Document supported video formats and size limits
- [ ] Add examples of proper file paths
- [ ] Document YouTube embed URL format requirements

### Code Comments
- [x] Comment each case in video loading logic
- [x] Explain YouTube URL conversion process
- [x] Document os.path.isfile() vs os.path.exists()
- [ ] Add inline examples in comments
- [ ] Document edge cases and limitations

---

## 🚀 Deployment Checklist

### Pre-Deployment
- [ ] Run full test suite (unit + integration)
- [ ] Test on clean database (no demo content)
- [ ] Test with fresh uploads directory
- [ ] Verify all error messages are user-friendly
- [ ] Check logs for unexpected warnings/errors
- [ ] Performance test with large video files (>100MB)

### Post-Deployment
- [ ] Monitor error logs for file loading failures
- [ ] Track YouTube embed success rate
- [ ] Collect user feedback on video playback
- [ ] Monitor storage usage for uploaded videos
- [ ] Set up alerts for repeated file access errors

---

## 📊 Success Criteria

- [x] ✅ YouTube videos load using embed URLs
- [x] ✅ Local files validated with `os.path.isfile()`
- [x] ✅ Error handling prevents app crashes
- [x] ✅ User-friendly error messages with path details
- [ ] 🔄 All file paths are absolute or documented as relative
- [ ] 🔄 Database stores embed URLs for YouTube content
- [ ] 🔄 100% test coverage for video loading scenarios
- [ ] 🔄 Documentation complete and up-to-date

---

## 🔗 Related Files

- `demo_app.py` - Main app with video selector and search
- `library_view.py` - Library display with grid/list playback
- `upload_ui.py` - Upload interface with file validation
- `content_index.db` - Content metadata database
- `ARCHITECTURE.md` - System architecture documentation

---

## 📌 Priority Items

### High Priority (Complete Before Login)
- [x] YouTube embed URL detection and conversion
- [x] Local file validation with `os.path.isfile()`
- [x] Error handling with fallback messages
- [ ] File path verification (absolute vs relative)
- [ ] Upload directory structure creation

### Medium Priority (Complete Before Beta)
- [ ] Database schema updates (storage_type column)
- [ ] Migration script for existing URLs
- [ ] Comprehensive testing suite
- [ ] Documentation updates

### Low Priority (Post-Launch)
- [ ] Unit tests for all helper functions
- [ ] Advanced YouTube features (playlists, timestamps)
- [ ] Performance optimization for large files
- [ ] CDN integration for video delivery

---

## 🎯 Current Status

**Phase 1: Core Implementation** ✅ Complete
- YouTube URL detection and embed conversion
- Local file validation with `os.path.isfile()`
- Error handling with user-friendly messages
- Applied across all video/audio display locations

**Phase 2: Path & Storage** 🚧 In Progress
- File path verification
- Database schema updates
- Upload directory structure

**Phase 3: Testing & Docs** 📋 Planned
- Comprehensive test suite
- Documentation updates
- Migration scripts
