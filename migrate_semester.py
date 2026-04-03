import os
import sqlite3

def migrate_semester():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'nsrit_portal.db')
    print(f"Connecting to {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if current_semester already exists
        cursor.execute("PRAGMA table_info(students)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'current_semester' not in columns:
            print("Adding current_semester column to students table...")
            cursor.execute("ALTER TABLE students ADD COLUMN current_semester VARCHAR(10) DEFAULT '1-1'")
            conn.commit()
            print("Column added successfully.")
        else:
            print("current_semester column already exists.")

        # Update existing data based on year
        print("Updating existing current_semester data based on year...")
        # year 1 -> 1-2
        cursor.execute("UPDATE students SET current_semester = '1-2' WHERE year = 1")
        # year 2 -> 2-2 
        cursor.execute("UPDATE students SET current_semester = '2-2' WHERE year = 2")
        # year 3 -> 3-2
        cursor.execute("UPDATE students SET current_semester = '3-2' WHERE year = 3")
        # year 4 -> 4-2
        cursor.execute("UPDATE students SET current_semester = '4-2' WHERE year = 4")
        
        conn.commit()
        print("Data updated successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate_semester()
