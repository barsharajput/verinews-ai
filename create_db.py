import os
import sqlite3

db_path = os.path.join(os.path.dirname(__file__), "app.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    result TEXT,
    confidence REAL,
    user_id INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")
