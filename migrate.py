import os
from utils.db import get_db_connection

def migrate_db():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to db")
        return
        
    cursor = conn.cursor()
    try:
        # Truncate strings to prevent Data Truncation error when altering table
        print("Updating existing student passwords to 'Pass123!'")
        cursor.execute("UPDATE students SET password_hash = 'Pass123!'")
        
        print("Updating existing admin passwords to 'Admin12!'")
        cursor.execute("UPDATE admins SET password_hash = 'Admin12!'")
        
        # SQLite does not support MODIFY. We will just perform the data update.
        # If the schema needs changing, it requires creating a temp table in SQLite.
        conn.commit()
        print("Data update complete!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error migrating DB: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    migrate_db()
