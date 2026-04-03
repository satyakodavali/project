import sqlite3
import os

db_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\backend\nsrit_portal.db'
schema_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\database\schema.sql'
seed_path = r'c:\Users\LENOVO\NewCollegeChatBot\college-portal\database\seed_data.sql'

def reseed():
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Executing schema...")
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())
    
    print("Executing seed data (this might take a moment for 1000 students)...")
    with open(seed_path, 'r') as f:
        # Executescript handles multiple INSERT statements
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()
    print("Reseed complete!")

if __name__ == "__main__":
    reseed()
