import sqlite3
import bcrypt

DB_PATH = 'backend/database/pentecost_church.db'
vals = [
    ('admin@pentecostchurch.org', 'admin123'),
    ('grace@example.com', 'password'),
    ('pastor@example.com', 'password'),
]

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for email, pwd in vals:
    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    cur.execute('UPDATE users SET password_hash = ? WHERE email = ?', (hashed, email))
    print(f'Updated {email}')

conn.commit()
conn.close()
