import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'nsrit_portal.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create exam_timetables table
cursor.execute("""
CREATE TABLE IF NOT EXISTS exam_timetables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    branch VARCHAR(50) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    exam_type VARCHAR(20) NOT NULL,
    schedule_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Pre-populate with some sample data for 1-1 to 4-2 if needed,
# or we'll generate it dynamically.
# For now, just ensure the table exists.

conn.commit()
conn.close()
print("Database updated successfully.")
