import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('pentecost_church.db')
SCHEMA_PATH = Path(__file__).with_name('schema.sql')
SEED_PATH = Path(__file__).with_name('seed.sql')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    with SCHEMA_PATH.open('r', encoding='utf-8') as schema_file:
        conn.executescript(schema_file.read())

    with SEED_PATH.open('r', encoding='utf-8') as seed_file:
        conn.executescript(seed_file.read())

    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()
    print(f'Initialized SQLite database at {DB_PATH}')
