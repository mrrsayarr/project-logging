
"""
Verileri eventdescription tablosuna ekleme fonksiyonu
Sütun başlarında EventID ve Description başlıkları olmak zorunda
"""

import sqlite3
import pandas as pd


def add_events_from_excel(db_path, excel_path, sheet_name='Sheet1'):
    # Excel dosyasını oku
    df = pd.read_excel(excel_path, sheet_name=sheet_name)

    # Veritabanına bağlanma
    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    # DataFrame'deki her satırı tabloya ekle
    for index, row in df.iterrows():
        cursor.execute('''
            INSERT OR IGNORE INTO eventdescription (EventID, Description)
            VALUES (?, ?)
        ''', (row['EventID'], row['Description']))

    # Değişiklikleri kaydetme
    db.commit()
    db.close()


# Örnek kullanım
if __name__ == "__main__":
    add_events_from_excel('Database.db', 'data.xlsx') # Verileri Database.db içine ekleme. (data.xlsx dosyasını kullanarak)
