# System Architecture - Unified Content Hub

## Architecture Overview

This document describes the complete data flow from user action through cloud sync to playback/download.

```
┌─────────────────────────────────────────────────────────────┐
│                        User Action                          │
│                 (Browse, Search, Upload)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     Hub Interface                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Drop-down: [Student | Practitioner | Author]        │   │
│  │ Search bar: [________] [Type: All ▼] [Sort: ▼]     │   │
│  │ Filters: Tags, Date, Author                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────┬───────────────┬──────────────────┐      │
│  │ 🎥 Video     │ 🎵 Audio      │ 📚 Book/Doc      │      │
│  │ Loader       │ Loader        │ Loader           │      │
│  │              │               │                  │      │
│  │ [Upload]     │ [Upload]      │ [Upload]         │      │
│  │ Metadata     │ Metadata      │ Metadata         │      │
│  │ Preview      │ Preview       │ Preview          │      │
│  └──────────────┴───────────────┴──────────────────┘      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                     Sync Manager                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Upload Pipeline:                                    │   │
│  │  1. Validate file (type, size, virus scan)         │   │
│  │  2. Compress (reduce bandwidth usage)              │   │
│  │  3. Encrypt (AES-256)                              │   │
│  │  4. Upload to cloud storage                        │   │
│  │  5. Generate signed URL                            │   │
│  │  6. Insert metadata into DB                        │   │
│  │  7. Return success/error to user                   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Download Pipeline:                                  │   │
│  │  1. Check user permissions                         │   │
│  │  2. Generate temporary signed URL (1-hour expiry)  │   │
│  │  3. Stream content from cloud                      │   │
│  │  4. Decrypt on-the-fly                             │   │
│  │  5. Cache locally (optional)                       │   │
│  │  6. Track view/download event                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Conflict Resolution:                                │   │
│  │  • Detect: Same content modified on multiple devices│   │
│  │  • Strategy: Last-write-wins (timestamp-based)     │   │
│  │  • Notify: User sees "Synced" or "Conflict" badge  │   │
│  │  • Manual: User can choose which version to keep   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Cloud Storage + Metadata DB                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Cloud Storage (Azure Blob / AWS S3 / GCP Storage)  │   │
│  │  • Encrypted at rest                               │   │
│  │  • Geo-redundant (multiple regions)                │   │
│  │  • Lifecycle policies (archive old content)        │   │
│  │  • CDN for fast global access                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Metadata Database (PostgreSQL / Cloud SQL)         │   │
│  │                                                     │   │
│  │ content:                                            │   │
│  │  - id, title, type, tags, description              │   │
│  │  - author, institution, license                    │   │
│  │  - cloud_url, encryption_key_id                    │   │
│  │  - added_at, updated_at                            │   │
│  │  - uploaded_by, target_role                        │   │
│  │  - purchase_status (free | purchased | rented)     │   │
│  │  - price, rental_days                              │   │
│  │                                                     │   │
│  │ users:                                              │   │
│  │  - id, username, email, password_hash              │   │
│  │  - role (student | practitioner | author | admin)  │   │
│  │  - created_at, last_login                          │   │
│  │                                                     │   │
│  │ permissions:                                        │   │
│  │  - user_id, content_id, access_level               │   │
│  │  - can_view, can_download, can_edit, can_share    │   │
│  │  - expires_at (for rentals)                        │   │
│  │                                                     │   │
│  │ purchases:                                          │   │
│  │  - user_id, content_id, purchase_type              │   │
│  │  - price_paid, purchased_at                        │   │
│  │  - transaction_id, payment_status                  │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   User Library View                         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ My Library                                          │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │ Search: [_________]  Filters: [Type ▼] [Role ▼] │ │   │
│  │ │                              [Date ▼] [Status ▼] │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  │                                                     │   │
│  │ Dynamic Content List:                               │   │
│  │                                                     │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │ 🎥 "Introduction to Ethics in AI"               │ │   │
│  │ │    Author: Dr. Jane Smith                       │ │   │
│  │ │    Tags: ethics, ai, philosophy                 │ │   │
│  │ │    Type: Video | Duration: 45:30                │ │   │
│  │ │    Status: ✅ Purchased | Added: 2025-11-20     │ │   │
│  │ │    [▶ Play] [📥 Download] [⭐ Rate]             │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  │                                                     │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │ 📚 "Philosophy of AI"                           │ │   │
│  │ │    Author: Multiple Contributors                │ │   │
│  │ │    Tags: ethics, ai, textbook                   │ │   │
│  │ │    Type: Book (PDF) | Pages: 450                │ │   │
│  │ │    Status: 🔓 Free | Added: 2025-11-15          │ │   │
│  │ │    [📖 Read] [📥 Download] [💬 Comment]        │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  │                                                     │   │
│  │ ┌─────────────────────────────────────────────────┐ │   │
│  │ │ 🎵 "Week 3 Lecture: Ethical Frameworks"         │ │   │
│  │ │    Author: user-001 (Practitioner)              │ │   │
│  │ │    Tags: lecture, week3, ethics                 │ │   │
│  │ │    Type: Audio | Duration: 30:15                │ │   │
│  │ │    Status: 📤 My Upload | Added: 2025-11-23     │ │   │
│  │ │    [▶ Play] [✏️ Edit] [🗑️ Delete]              │ │   │
│  │ └─────────────────────────────────────────────────┘ │   │
│  │                                                     │   │
│  │ Filter Results:                                     │   │
│  │  • Shows content user has purchased                │   │
│  │  • Shows content user has uploaded                 │   │
│  │  • Shows free public content                       │   │
│  │  • Metadata displayed even if title forgotten      │   │
│  │  • Searchable by any field (title, author, tags)   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Playback / Download                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Video Playback:                                     │   │
│  │  • Inline HTML5 video player                       │   │
│  │  • Streaming from cloud (HLS/DASH)                 │   │
│  │  • Quality selection (360p, 720p, 1080p)           │   │
│  │  • Playback speed control (0.5x - 2x)              │   │
│  │  • Captions/Subtitles support                      │   │
│  │  • Resume from last position                       │   │
│  │  • Picture-in-picture mode                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Audio Playback:                                     │   │
│  │  • HTML5 audio player                              │   │
│  │  • Streaming or progressive download               │   │
│  │  • Waveform visualization                          │   │
│  │  • Playback speed control                          │   │
│  │  • Background playback                             │   │
│  │  • Playlist support                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Document Viewer:                                    │   │
│  │  • Inline PDF viewer (pdf.js)                      │   │
│  │  • Page navigation                                 │   │
│  │  • Zoom controls                                   │   │
│  │  • Search within document                          │   │
│  │  • Annotations/Highlights                          │   │
│  │  • Download for offline reading                    │   │
│  │  • Print functionality                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Analytics Tracking:                                 │   │
│  │  • Log view event (content_id, user_id, timestamp) │   │
│  │  • Track playback progress (watched duration)      │   │
│  │  • Track completion status                         │   │
│  │  • Track downloads                                 │   │
│  │  • Generate engagement metrics                     │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Role-Based Access Control

### Student Role
**Permissions:**
- ✅ Search all public content
- ✅ View purchased content
- ✅ Download purchased content
- ✅ Track progress (viewed/skipped)
- ❌ Cannot upload content
- ❌ Cannot edit content
- ❌ Cannot access practitioner materials

**UI View:**
- Search bar + filters
- Library view (purchased + free content)
- Playback controls
- No upload interface

### Practitioner Role
**Permissions:**
- ✅ All Student permissions
- ✅ Upload videos, audio, documents
- ✅ Create homework assignments
- ✅ Manage sessions
- ✅ View student progress
- ✅ Edit/delete own uploads
- ❌ Cannot publish to library catalog

**UI View:**
- Upload interface (Video, Audio, Book loaders)
- Session management tools
- Student progress dashboard
- All Student features

### Author Role
**Permissions:**
- ✅ All Practitioner permissions
- ✅ Upload curated library content
- ✅ Add attribution metadata (institution, license, DOI)
- ✅ Publish to library catalog
- ✅ Set pricing (free, paid, rental)
- ✅ View analytics (downloads, ratings, revenue)
- ✅ Edit/update published content

**UI View:**
- Advanced upload with attribution fields
- Publishing workflow
- Analytics dashboard
- Revenue tracking
- All Practitioner features

### Admin Role
**Permissions:**
- ✅ All Author permissions
- ✅ Manage users (create, edit, delete)
- ✅ Manage all content (regardless of owner)
- ✅ Configure system settings
- ✅ View system-wide analytics
- ✅ Moderate content (approve/reject)
- ✅ Handle disputes

**UI View:**
- User management interface
- Content moderation queue
- System configuration panel
- All Author features

## Data Flow Examples

### Example 1: Practitioner Uploads Video
```
1. Practitioner switches role to "Practitioner"
2. Sees upload interface with Video loader
3. Selects video file (lecture_week3.mp4, 150MB)
4. Fills metadata:
   - Title: "Week 3: Ethical Frameworks"
   - Tags: "lecture, week3, ethics"
   - Description: "Introduction to ethical frameworks in AI"
5. Clicks "Upload Video"
6. Sync Manager:
   - Validates file (MP4, 150MB < 500MB limit)
   - Compresses (150MB → 120MB)
   - Encrypts (AES-256)
   - Uploads to cloud storage
   - Generates URL: https://cdn.example.com/videos/abc123.mp4
   - Inserts metadata into database
7. Success message: "Video uploaded successfully!"
8. Video now appears in search results for students
```

### Example 2: Student Searches and Plays Video
```
1. Student searches "ethical frameworks"
2. Search query:
   SELECT * FROM content 
   WHERE (title LIKE '%ethical frameworks%' OR tags LIKE '%ethical frameworks%')
   AND (target_role = 'all' OR target_role = 'student')
   AND (purchase_status = 'free' OR content_id IN (SELECT content_id FROM purchases WHERE user_id = ?))
3. Results show "Week 3: Ethical Frameworks"
4. Student clicks "Play"
5. Sync Manager:
   - Checks permissions (student has access to free practitioner content)
   - Generates temporary signed URL (1-hour expiry)
   - Returns URL to player
6. Video streams from cloud
7. Progress tracked:
   - INSERT INTO viewing_history (user_id, content_id, watched_duration, timestamp)
8. On completion:
   - UPDATE viewing_history SET status = 'completed'
```

### Example 3: Author Publishes Book with Pricing
```
1. Author switches role to "Author"
2. Uses Book/Document loader
3. Uploads book (ethics_textbook.pdf, 25MB)
4. Fills metadata:
   - Title: "Ethics in AI: A Comprehensive Guide"
   - Author: "Dr. Jane Smith"
   - Institution: "University of Example"
   - License: "CC BY-SA"
   - Tags: "ethics, ai, textbook, comprehensive"
   - Description: "Complete textbook covering ethical considerations..."
5. Sets pricing:
   - Type: "Paid"
   - Price: $29.99
   - Allow rental: Yes ($4.99 for 30 days)
6. Clicks "Publish to Library"
7. Content enters moderation queue
8. Admin approves → content goes live
9. Students can purchase or rent
10. Author receives revenue share (70% of sales)
```

## Security & Privacy

### Encryption
- **At Rest:** All files encrypted with AES-256
- **In Transit:** TLS 1.3 for all connections
- **Keys:** Stored in Azure Key Vault / AWS Secrets Manager
- **Rotation:** Keys rotated every 90 days

### Authentication
- **Method:** OAuth 2.0 (Google, Microsoft, GitHub)
- **Session:** JWT tokens with 1-hour expiry
- **Refresh:** Automatic token refresh
- **MFA:** Optional two-factor authentication

### Authorization
- **Model:** Role-Based Access Control (RBAC)
- **Enforcement:** Checked on every request
- **Audit:** All access logged
- **Principle:** Least privilege (deny by default)

### Data Privacy
- **Isolation:** User data strictly isolated
- **Compliance:** GDPR, CCPA, FERPA compliant
- **Retention:** Configurable retention policies
- **Deletion:** Right to be forgotten (complete data deletion)

## Performance Considerations

### Caching
- **CDN:** CloudFlare for global content delivery
- **Local:** Browser cache for frequently accessed content
- **Redis:** In-memory cache for metadata

### Optimization
- **Compression:** Gzip/Brotli for text, H.265 for video
- **Lazy Loading:** Load content on-demand
- **Pagination:** 20 items per page in search results
- **Indexing:** Database indexes on title, tags, author, added_at

### Scalability
- **Load Balancing:** Multiple app servers behind load balancer
- **Database:** Read replicas for scalability
- **Storage:** Object storage scales infinitely
- **CDN:** Global edge locations for low latency

## Monitoring & Analytics

### System Health
- **Uptime:** Monitor 99.9% SLA
- **Response Time:** <500ms for searches, <5s for uploads
- **Error Rate:** <0.1% of requests
- **Storage:** Monitor usage and costs

### User Analytics
- **Engagement:** Time spent, completion rates
- **Popular Content:** Most viewed, most downloaded
- **Search Patterns:** Common queries, no-result searches
- **Conversion:** Free → Paid conversion rate

### Business Metrics
- **Revenue:** Sales, rentals, subscriptions
- **Growth:** New users, active users, retention
- **Content:** Upload rate, approval rate
- **Performance:** ROI, CAC, LTV

---

**Status:** Phase 1 Complete ✅ | Phase 2 In Progress 🚧 | Phase 3 Planned 📋
