import sqlite3

db_path = 'nsrit_portal.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='semester_results'")
row = cursor.fetchone()
if row:
    print(row[0])
conn.close()
