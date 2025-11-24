"""
Database Migration Script
Migrates content_index.db to comprehensive metadata schema
"""
import sqlite3
import os
from datetime import datetime


def migrate_database():
    """Migrate existing database to new schema"""
    db_path = "content_index.db"
    
    if not os.path.exists(db_path):
        print(f"✓ No existing database found at {db_path}")
        print("  New schema will be created on first run")
        return
    
    print(f"🔄 Migrating database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get current schema
    cursor.execute("PRAGMA table_info(content)")
    columns = {col[1]: col for col in cursor.fetchall()}
    
    print(f"   Current columns: {list(columns.keys())}")
    
    # Add new columns if they don't exist
    migrations = [
        ("author", "TEXT"),
        ("user_role", "TEXT DEFAULT 'student'"),
        ("source", "TEXT DEFAULT 'local_file'"),
        ("url", "TEXT"),
        ("purchase_status", "TEXT DEFAULT 'uploaded'"),
        ("description", "TEXT"),
        ("uploaded_by", "TEXT"),
    ]
    
    for column_name, column_type in migrations:
        if column_name not in columns:
            print(f"   ➕ Adding column: {column_name} {column_type}")
            cursor.execute(f"ALTER TABLE content ADD COLUMN {column_name} {column_type}")
        else:
            print(f"   ✓ Column exists: {column_name}")
    
    # Migrate data: Set source based on path content
    print(f"\n🔄 Migrating existing data...")
    cursor.execute("SELECT id, path FROM content WHERE source IS NULL OR source = ''")
    rows = cursor.fetchall()
    
    for item_id, path in rows:
        if path:
            if "youtube.com" in path or "youtu.be" in path:
                source = "youtube_link"
                # Convert to embed URL if watch URL
                if "watch?v=" in path:
                    video_id = path.split("watch?v=")[-1].split("&")[0]
                    url = f"https://www.youtube.com/embed/{video_id}"
                elif "youtu.be" in path:
                    video_id = path.split("/")[-1]
                    url = f"https://www.youtube.com/embed/{video_id}"
                else:
                    url = path
                
                cursor.execute("""
                    UPDATE content 
                    SET source = ?, url = ?, path = NULL 
                    WHERE id = ?
                """, (source, url, item_id))
                print(f"   ✓ Migrated YouTube video ID {item_id}: {url}")
                
            elif path.startswith("http://") or path.startswith("https://"):
                source = "external_url"
                cursor.execute("""
                    UPDATE content 
                    SET source = ?, url = ?, path = NULL 
                    WHERE id = ?
                """, (source, path, item_id))
                print(f"   ✓ Migrated external URL ID {item_id}: {path}")
                
            else:
                source = "local_file"
                cursor.execute("""
                    UPDATE content 
                    SET source = ? 
                    WHERE id = ?
                """, (source, item_id))
                print(f"   ✓ Migrated local file ID {item_id}: {path}")
    
    # Set default values for other fields
    cursor.execute("""
        UPDATE content 
        SET user_role = 'practitioner' 
        WHERE user_role IS NULL OR user_role = ''
    """)
    
    cursor.execute("""
        UPDATE content 
        SET purchase_status = 'curated' 
        WHERE purchase_status IS NULL OR purchase_status = ''
    """)
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Migration completed successfully!")
    print(f"   Database: {db_path}")
    print(f"   Schema updated with comprehensive metadata")


if __name__ == "__main__":
    print("=" * 60)
    print("Content Database Migration Script")
    print("=" * 60)
    print()
    
    try:
        migrate_database()
        print()
        print("=" * 60)
        print("✅ Migration Complete!")
        print("=" * 60)
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ Migration Failed: {e}")
        print("=" * 60)
        raise
