# database.py
import sqlite3

conn = sqlite3.connect('artworks.db')
cursor = conn.cursor()


cursor.execute("DROP TABLE IF EXISTS artworks")


create_table_sql = """
CREATE TABLE artworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artwork_uuid TEXT NOT NULL UNIQUE, -- The new random, unique text ID
    artist_name TEXT NOT NULL,
    artwork_title TEXT NOT NULL,
    date_added TEXT NOT NULL,
    image_filename TEXT, -- Stores the filename of the uploaded image

    -- Administrative & Logistical
    current_location TEXT,
    artwork_value REAL,
    
    -- Physical Attributes
    materials TEXT,
    dimensions TEXT,
    signature_details TEXT,
    condition_notes TEXT,
    
    -- Contextual & Descriptive
    subject_content TEXT,
    description TEXT,
    exhibition_history TEXT,
    provenance TEXT,
    bibliography TEXT
);
"""

cursor.execute(create_table_sql)
conn.commit()
conn.close()

print("Database 'artworks.db' and new 'artworks' table created successfully.")