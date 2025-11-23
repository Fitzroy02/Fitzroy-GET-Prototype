---
name: Video Loading Improvements
about: Fix video/audio loading with proper file handling and YouTube embed support
title: "[Enhancement] Improve Video/Audio Loading with Embed Support"
labels: enhancement, bug fix
assignees: ''
---

## Problem Statement
Video and audio loading needs proper handling for both local files and remote URLs, with special support for YouTube embed URLs.

## Tasks

### YouTube Embed URL Support
- [x] Update `demo_app.py` to use embed URLs for YouTube videos
- [x] Create `convert_youtube_url()` helper function to transform watch URLs to embed format
- [x] Handle `youtube.com/watch?v=VIDEO_ID` format
- [x] Handle `youtu.be/VIDEO_ID` short URL format
- [x] Extract video ID using regex pattern matching
- [x] Apply to Home page video player
- [x] Apply to Search results video display
- [x] Apply to Library view video playback

### Local File Handling
- [x] Ensure local files are opened with `open(path, "rb")` before passing to `st.video()`
- [x] Create `load_video()` helper function for unified loading
- [x] Create `load_audio()` helper function for unified loading
- [x] Read file contents in binary mode for proper streaming
- [x] Apply to all video display locations
- [x] Apply to all audio display locations

### File Existence Verification
- [ ] Verify that uploaded video files exist in `uploads/videos/` directory
- [ ] Verify that uploaded audio files exist in `uploads/audios/` directory
- [ ] Verify that uploaded book files exist in `uploads/books/` directory
- [ ] Check demo content paths (`/user/storage/videos/demo1.mp4`, etc.)
- [ ] Update demo content paths to use actual existing files
- [ ] Create test files in appropriate directories for development

### Error Handling
- [x] Add error handling: if file not found, show user-friendly message instead of crashing
- [x] Implement try-except blocks around file operations
- [x] Show `st.error()` message for FileNotFoundError
- [x] Show `st.warning()` message for other exceptions
- [x] Provide fallback to URL path if binary read fails
- [x] Return None from helper functions on error to prevent rendering
- [x] Test error handling with missing files
- [x] Test error handling with invalid paths

### Database Schema Updates
- [ ] Update Library metadata schema to distinguish between local files and external embeds
- [ ] Add `storage_type` column to content table (values: "local", "url", "youtube")
- [ ] Add `original_url` column to preserve YouTube watch URLs
- [ ] Update `upload_content()` to set storage_type based on input
- [ ] Update search queries to handle different storage types
- [ ] Add migration script to update existing records
- [ ] Document schema changes in ARCHITECTURE.md

### Testing & Validation
- [x] Test YouTube watch URL conversion to embed format
- [x] Test YouTube short URL (youtu.be) conversion
- [ ] Test local video file upload and playback
- [ ] Test local audio file upload and playback
- [ ] Test book/document file upload and download
- [ ] Test with missing local files (should show error, not crash)
- [ ] Test with invalid URLs (should show warning)
- [ ] Test with mixed content (local + YouTube + external URLs)
- [ ] Verify error messages are user-friendly
- [ ] Test across all pages: Home, Library, Search, Upload

### Code Quality
- [x] Apply DRY principle (Don't Repeat Yourself) with helper functions
- [x] Consolidate duplicate video/audio loading logic
- [x] Add docstrings to all helper functions
- [x] Use consistent error handling patterns
- [ ] Add unit tests for helper functions
- [ ] Add integration tests for video loading workflows
- [ ] Update inline comments for clarity

### Documentation
- [ ] Document `convert_youtube_url()` usage in code comments
- [ ] Document `load_video()` and `load_audio()` functions
- [ ] Update ARCHITECTURE.md with video loading flow
- [ ] Add examples of proper video URL formats
- [ ] Document storage_type schema in database section
- [ ] Create troubleshooting guide for video loading issues

## Implementation Status

### ✅ Completed (Phase 1)
- YouTube embed URL conversion
- Helper functions: `convert_youtube_url()`, `load_video()`, `load_audio()`
- Binary file reading for local files
- Error handling with user-friendly messages
- Applied across all video/audio display locations
- Unified loading logic (DRY principle)

### 🚧 In Progress (Phase 2)
- File existence verification
- Database schema updates for storage_type
- Comprehensive testing

### 📋 Planned (Phase 3)
- Unit and integration tests
- Documentation updates
- Migration scripts

## Success Criteria
- ✅ YouTube videos load using embed URLs without errors
- ✅ Local files are read in binary mode before display
- 🔄 All file paths are verified before use
- ✅ Graceful error handling with user-friendly messages
- 🔄 Database tracks storage type (local vs external)
- 🔄 No crashes from missing files or invalid paths
- ✅ Code follows DRY principle with reusable helper functions

## Related Files
- `demo_app.py` - Main app with video player
- `library_view.py` - Library display with playback
- `upload_ui.py` - Upload interface for content
- `content_index.db` - Content metadata database
- `ARCHITECTURE.md` - System architecture documentation

## Notes
- YouTube embed URLs provide better compatibility across devices
- Binary file reading ensures proper video streaming
- Error handling prevents app crashes and improves UX
- Storage type tracking enables future features (CDN migration, caching)
