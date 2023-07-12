import sqlite3


database = sqlite3.connect('translation.db')


cursor = database.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT,
        src TEXT,
        dest TEXT,
        original TEXT,
        translated TEXT
    );
''')

database.commit()
database.close()