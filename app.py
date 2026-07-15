from flask import Flask, render_template, request, redirect, session, url_for
from data_model import connect_user, create_user, get_user_by_id, update_user, get_user_transactions, add_book, get_books_by_owner, get_books_by_user, delete_book_by_id, get_book_by_id, update_book_by_id, search_books, get_favorite_books, mark_as_favorite, remove_favorite, get_messages, send_message, get_conversation
import sqlite3

app = Flask(__name__)
app.secret_key = 'ton_mot_de_passe_secret'


# ------------------ PAGE ACCUEIL ------------------

@app.route('/')
def index():
    return render_template('index.html')

# ------------------ CONNEXION ------------------

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user_id = connect_user(email, password)
    if user_id != -1:
        session['user_id'] = user_id
        user_info = get_user_by_id(user_id)
        session['user_name'] = user_info[0] if user_info else 'Utilisateur'
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error="Identifiants incorrects.")


# ------------------ INSCRIPTION ------------------

@app.route('/new_user', methods=['GET'])
def new_user():
    return render_template('new_user.html')

@app.route('/new_user', methods=['POST'])
def new_user_post():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    city = request.form['city']
    user_id = create_user(name, email, password, city)
    if user_id == -1:
        return render_template('new_user.html', error="L'utilisateur existe déjà.")
    session['user_id'] = user_id
    user_info = get_user_by_id(user_id)
    session['user_name'] = user_info[0] if user_info else 'Utilisateur'
    return redirect(url_for('index'))


# ------------------ PROFIL ------------------

@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    transactions = get_user_transactions(user_id)

    return render_template('profile.html', user=user, transactions=transactions)

@app.route('/profile/update', methods=['POST'])
def profile_update():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    city = request.form['city']

    update_user(user_id, name, email, password, city)


    session['user_name'] = name

    return redirect(url_for('profile'))


# ------------------ MODIFIER INFOS ------------------

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        city = request.form['city']
        password = request.form['password']
        update_user(user_id, name, email, password, city)
        session['user_name'] = name
        return redirect(url_for('profile'))

    user = get_user_by_id(user_id)
    return render_template('edit_profile.html', user=user)


# ------------------ TRANSACTIONS ------------------

@app.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    transactions = get_user_transactions(session['user_id'])
    return render_template('transactions.html', transactions=transactions)


# ------------------ DÉCONNEXION ------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ------------------ AJOUT DE LIVRES  ------------------

@app.route('/add_book_options')
def add_book_options():
    """
    Affiche une page où l'utilisateur choisit :
    - Donner ou emprunter un livre
    - Revendre un livre
    """
    return render_template('add_book_options.html')

@app.route('/add_book/<action>', methods=['GET'])
def show_add_book_form(action):
    """
    Affiche un formulaire d'ajout de livre selon l'action choisie.
    'action' peut être 'donner' ou 'vendre'.
    """
    return render_template('add_book.html', action=action)

@app.route('/submit_book', methods=['POST'])
def submit_book():
    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    image_url = request.form.get('image_url', '')  
    category = request.form['category'] 
    condition = request.form['condition']
    owner_id = session.get('user_id')
    price = float(request.form['price'])
    action = request.form.get('action')

    if owner_id:
        add_book(title, author, description, condition, category, image_url, owner_id, price, action)

    return redirect(url_for('mes_livres'))


# ------------------ MesLivre ------------------

@app.route('/mes_livres')
def mes_livres():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    books = get_books_by_user(user_id)

    return render_template('mes_livres.html', books=books)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    delete_book_by_id(book_id, session['user_id'])
    return redirect(url_for('mes_livres'))

@app.route('/edit_book/<int:book_id>', methods=['GET'])
def edit_book_get(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    book = get_book_by_id(book_id)
    if not book:
        return "Livre introuvable", 404

    return render_template('edit_book.html', book=book)



@app.route('/edit_book/<int:book_id>', methods=['POST'])
def edit_book_post(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    author = request.form['author']
    description = request.form['description']
    condition = request.form['condition']
    category = request.form['category']
    price = float(request.form['price'])
    status = request.form['status']
    action = request.form['action']

    update_book_by_id(book_id, title, author, description, condition, category, price, status, action )
    return redirect(url_for('mes_livres'))

# ------------------ favoris  ------------------
@app.route('/favorites')
def favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    books = get_favorite_books(session['user_id'])
    return render_template('favorites.html', books=books)


@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    book_id = request.form.get('book_id')
    mark_as_favorite(session['user_id'], book_id)
    return redirect(url_for('favorites'))


@app.route('/remove_favorite/<int:book_id>')
def remove_favorite_route(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    remove_favorite(session['user_id'], book_id)
    return redirect(url_for('favorites'))


# ------------------  page Bibliothèque avec recherche ----------------
@app.route('/books')
def books():
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    city = request.args.get('city', '')
    page = int(request.args.get('page', 1))
    per_page = 6

    books = search_books(keyword, category, city)

    total_books = len(books)
    total_pages = (total_books + per_page - 1) // per_page  
    start = (page - 1) * per_page
    end = start + per_page
    paginated_books = books[start:end]
    return render_template('books.html',books=books,keyword=keyword,category=category,city=city,page=page, total_pages=total_pages)


@app.route('/book/<int:book_id>')
def book_details(book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
  SELECT 
    b.title, b.author, b.description, b.image_url,
    b.condition, b.category, b.status, u.name, u.city,
    b.price, b.action,  b.owner_id
  FROM books b
  JOIN users u ON b.owner_id = u.id
  WHERE b.id=?
""", (book_id,))

    book = cursor.fetchone()
    conn.close()
    if not book:
        return "Livre introuvable", 404
    
    book_owner_id = book[11]
    return render_template("book_details.html", book=book, book_id=book_id, book_owner_id=book_owner_id)

# ------------------ Page détails d'un livre qui est dans favoris  ----------------

@app.route('/favorites/book/<int:book_id>')
def favorite_book_details(book_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.title, b.author, b.description, b.image_url,
            b.condition, b.category, b.status, u.name, u.city,
            b.price, b.action
        FROM books b
        JOIN users u ON b.owner_id = u.id
        WHERE b.id = ?
    """, (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        return "Livre introuvable", 404
    
    return render_template("favorite_book_details.html", book=book)


# ------------------ Page messagerie   ----------------

@app.route('/messages')
def messages():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    messages = get_messages(user_id)
    return render_template("messages.html", messages=messages)

@app.route('/send_message', methods=['POST'])
def send_message_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    sender_id = session['user_id']
    receiver_id = request.form['receiver_id']
    book_id = request.form['book_id']
    content = request.form['content']

    send_message(sender_id, receiver_id, book_id, content)
    return redirect(url_for('messages'))


# ------------------Conversation  ------------------

@app.route('/conversation/<int:book_id>/<int:user_id>', methods=['GET', 'POST'])
def conversation(book_id, user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user_id = session['user_id']

    if request.method == 'POST':
        content = request.form['content']
        send_message(current_user_id, user_id, book_id, content)
    
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE messages 
    SET is_read = 1 
    WHERE book_id = ? AND sender_id = ? AND receiver_id = ? AND is_read = 0
    """, (book_id, user_id, current_user_id))
    conn.commit()
    conn.close()

    messages = get_conversation(current_user_id, user_id, book_id)
    return render_template("conversation.html", messages=messages, book_id=book_id, user_id=user_id)


# ------------------ LANCEMENT SERVEUR ------------------

if __name__ == '__main__':
    app.run(debug=True)
