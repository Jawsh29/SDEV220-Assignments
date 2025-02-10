from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f" {self.title} - {self.id} - {self.author} - {self.publisher}>"


# Get List of Books
@app.route('/books')
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'ID': book.id, 'Title': book.title, 'Author': book.author, 'Publisher': book.publisher}
        output.append(book_data)

    return {"books": output}

# Search Book by ID
@app.route('/books/<book_id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"Title": book.title, "Author": book.author, "Publisher": book.publisher}

# Add Book
@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json.get('title'), author=request.json.get('author'), publisher=request.json.get('publisher'))
    db.session.add(book)
    db.session.commit()
    return {'ID': book.id,"Title": book.title, "Author": book.author, "Publisher": book.publisher}

# Delete Book
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {'error': 'Book not found'}
    db.session.delete(book)
    db.session.commit()
    return {"Book Deleted"}


