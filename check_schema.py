"""Check database schema for Instagram columns."""
import sqlite3
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

def check_schema():
    """Check all columns in users table."""
    
    # Parse SQLite database URL
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    
    print(f"📋 Database: {db_path}")
    print("\n📊 Current users table schema:")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all columns
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        for col in columns:
            print(f"  {col[1]:30} {col[2]}")
        
        print("\n🔍 Required Instagram columns:")
        required = [
            "instagram_access_token",
            "instagram_refresh_token",
            "instagram_user_id",
            "instagram_username",
            "instagram_business_account_id",
            "instagram_connected_at"
        ]
        
        existing = {col[1] for col in columns}
        missing = [col for col in required if col not in existing]
        
        if missing:
            print(f"  ❌ Missing: {', '.join(missing)}")
        else:
            print(f"  ✅ All columns exist!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_schema()
