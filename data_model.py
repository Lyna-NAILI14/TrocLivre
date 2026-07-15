import sqlite3

def connect_user(email, password):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else -1

def create_user(name, email, password, city):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password, city) 
            VALUES (?, ?, ?, ?)
        ''', (name, email, password, city))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        return -1  
    conn.close()
    return user_id

# ------------------ Page profile ------------------


def get_user_by_id(user_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, city FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_user(user_id, name, email, password, city):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET name=?, email=?, password=?, city=?
        WHERE id=?
    """, (name, email, password, city, user_id))
    conn.commit()
    conn.close()

def get_user_transactions(user_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaction_type, status, created_at 
        FROM transactions 
        WHERE owner_id=? OR recipient_id=?
        ORDER BY created_at DESC
    """, (user_id, user_id))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

# ------------------ FONCTIONS POUR LES LIVRES ------------------
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_book(title, author, description, condition, category, image_url, owner_id, price, action  ): 
    """
    Ajoute un livre dans la base de données.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (title, author, description, condition, category, image_url, owner_id, price, action )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, description, condition, category, image_url, owner_id, price, action ))
    conn.commit()
    conn.close()

def delete_book(book_id, owner_id):
    """
    Supprime un livre appartenant à un utilisateur.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM books
        WHERE id = ? AND owner_id = ?
    ''', (book_id, owner_id))
    conn.commit()
    conn.close()



# ------------------ Afficher mes livre dans une page  ------------------
def get_books_by_owner(owner_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, author, description, image_url, category, condition, price, status, created_at, action
        FROM books
        WHERE owner_id=?
        ORDER BY created_at DESC
    """, (owner_id,))
    livres = cursor.fetchall()
    conn.close()
    return livres


def get_books_by_user(user_id):
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE owner_id=?', (user_id,))
    books = cursor.fetchall()
    conn.close()
    return books

def delete_book_by_id(book_id, user_id):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=? AND owner_id=?', (book_id, user_id))
    conn.commit()
    conn.close()

def get_book_by_id(book_id):
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

def update_book_by_id(book_id, title, author, description, condition, category, price, status, action ):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books 
        SET title=?, author=?, description=?, condition=?, category=?, price=?, status=?, action=?
        WHERE id=?
    ''', (title, author, description, condition, category, price, status, action, book_id))
    conn.commit()
    conn.close()


def search_books(keyword, category, city):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    query = """
        SELECT b.id, b.title, b.author, b.description, b.image_url, 
               b.condition, b.category, b.status, b.price, u.city
        FROM books b
        JOIN users u ON b.owner_id = u.id
        WHERE 1=1
    """
    params = []

    if keyword:
        query += " AND (b.title LIKE ? OR b.author LIKE ? OR b.description LIKE ?)"
        params.extend([f"%{keyword}%"] * 3)

    if category:
        query += " AND b.category = ?"
        params.append(category)

    if city:
        query += " AND u.city = ?"
        params.append(city)

    query += " ORDER BY b.created_at DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

  
# ------------------ Afficher mes favoris dans une page  ------------------
def mark_as_favorite(user_id, book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM favorites WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    already_favorite = cursor.fetchone()

    if not already_favorite:
        cursor.execute("INSERT INTO favorites (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        conn.commit()

    conn.close()


def get_favorite_books(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.id, b.title, b.image_url
        FROM books b
        JOIN favorites f ON b.id = f.book_id
        WHERE f.user_id = ?
    ''', (user_id,))
    books = cursor.fetchall()
    conn.close()
    return books

def remove_favorite(user_id, book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM favorites WHERE user_id = ? AND book_id = ?
    ''', (user_id, book_id))
    conn.commit()
    conn.close()

# ------------------ Afficher messagerie   ------------------

def send_message(sender_id, receiver_id, book_id, content):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, book_id, content)
        VALUES (?, ?, ?, ?)
    """, (sender_id, receiver_id, book_id, content))
    conn.commit()
    conn.close()

def get_messages(user_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m1.content, m1.created_at, b.title, u1.name AS sender, u2.name AS receiver, m1.book_id, 
               CASE 
                   WHEN m1.sender_id = ? THEN m1.receiver_id 
                   ELSE m1.sender_id 
               END AS other_user_id
        FROM messages m1
        JOIN (
            SELECT MAX(id) AS max_id
            FROM messages
            WHERE sender_id = ? OR receiver_id = ?
            GROUP BY 
                CASE 
                    WHEN sender_id < receiver_id THEN sender_id || '-' || receiver_id || '-' || book_id
                    ELSE receiver_id || '-' || sender_id || '-' || book_id
                END
        ) m2 ON m1.id = m2.max_id
        JOIN books b ON m1.book_id = b.id
        JOIN users u1 ON m1.sender_id = u1.id
        JOIN users u2 ON m1.receiver_id = u2.id
        ORDER BY m1.created_at DESC
    """, (user_id, user_id, user_id))

    rows = cursor.fetchall()
    messages = []
    for row in rows:
        content = row[0]
        created_at = row[1].split(" ")[0]  
        book_title = row[2]
        sender = row[3]
        receiver = row[4]
        book_id = row[5]
        other_user_id = row[6]
        messages.append((content, created_at, book_title, sender, receiver, book_id, other_user_id))
    conn.close()
    return messages



# ------------------ Conversation   ------------------
def get_conversation(user1_id, user2_id, book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.sender_id, u.name, m.content, m.created_at
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.book_id = ?
          AND ((m.sender_id = ? AND m.receiver_id = ?) OR (m.sender_id = ? AND m.receiver_id = ?))
        ORDER BY m.created_at ASC
    """, (book_id, user1_id, user2_id, user2_id, user1_id))
    rows = cursor.fetchall()
    messages = []
    for sender_id, sender_name, content, created_at in rows:
        date_only = created_at.split(" ")[0]
        messages.append((sender_id, sender_name, content, date_only))
    conn.close()
    return messages

