import sqlite3
import os

def show_database():
    # Database path
    db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'
    
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 1. Show Schema
        print("\n" + "="*80)
        print("  TABLE FORMAT (DATABASE SCHEMA)")
        print("="*80)
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students';")
        schema = cursor.fetchone()
        if schema:
            print(schema[0])
        else:
            print("Table 'students' not found.")
            return

        # 2. Show Data in Table Format
        print("\n" + "="*80)
        print("  DATA TABLE (ROWS & COLUMNS)")
        print("="*80)
        
        # Get column names
        cursor.execute('PRAGMA table_info(students)')
        columns = [c[1] for c in cursor.fetchall()]
        
        # Format for printing
        col_width = 18
        header = "".join([col.ljust(col_width) for col in columns])
        print(header)
        print("-" * len(header))

        # Get rows
        cursor.execute('SELECT * FROM students LIMIT 10')
        rows = cursor.fetchall()
        for row in rows:
            formatted_row = "".join([str(val).ljust(col_width) for val in row])
            print(formatted_row)
            
        print("\n" + "="*80)
        print("  Showing first 10 rows. Check 'nsrit_portal.db' in VS Code for more.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    show_database()
