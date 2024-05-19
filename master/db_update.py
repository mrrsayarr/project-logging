
"""
Database güncellemesini yapan fonksiyon
"""

import sqlite3

def update_database():
    db = sqlite3.connect('Database.db')
    cursor = db.cursor()

    """
    cursor.execute('''
        ALTER TABLE events
        ADD COLUMN PredictedValue NUMERIC
    ''')
    """

    """
    # Hata logları için tablo oluşturma
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS error_logs (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ErrorMessage TEXT,
            ErrorTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    """

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                SourceName TEXT,
                Title TEXT,
                PublishedAt TEXT,
                URL TEXT
            )
        ''')

    db.commit()
    db.close()

# Update için 1 defa çalıştırılır
if __name__ == "__main__":
    update_database()

