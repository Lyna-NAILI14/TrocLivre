import sqlite3
import json


conn = sqlite3.connect("books.db")
cursor = conn.cursor()

# --- Création des tables ---


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    city TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    image_url TEXT,
    category TEXT,
    condition TEXT,
    owner_id INTEGER,
    status TEXT DEFAULT 'disponible',
    price REAL DEFAULT 0,
    action TEXT DEFAULT 'donner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    owner_id INTEGER,
    recipient_id INTEGER,
    transaction_type TEXT,
    price INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')


cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
)
""")



cursor.execute('''
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
);
''')


conn.commit()
conn.close()

print("✅ Base de données créée avec succès.")
