import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'nsrit_portal.db')

def setup_database():
    print(f"Initializing SQLite Database at: {DB_PATH}")
    
    # Remove existing database if it exists to start fresh
    if os.path.exists(DB_PATH):
        print("Removing existing database file...")
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # 1. Execute Schema
        print("Creating tables from schema.sql...")
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            cursor.executescript(schema_sql)
            
        print("Tables created successfully!")
        
        # 2. Re-generate seed data (creates seed_data.sql)
        print("Generating new seed data...")
        import generate_seed 
        generate_seed.run()
        
        # 3. Execute Seed Data
        print("Inserting seed data from seed_data.sql...")
        seed_path = os.path.join(os.path.dirname(__file__), 'seed_data.sql')
        with open(seed_path, 'r') as f:
            seed_sql = f.read()
            cursor.executescript(seed_sql)
            
        conn.commit()
        print("\n✅ SQLite Database setup complete! Hashed credentials created.")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error setting up database: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    setup_database()
