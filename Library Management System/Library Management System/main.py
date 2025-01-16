from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List
import sqlite3

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Redirect root URL to the static index.html
@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

# Database setup
def init_db():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        genre TEXT,
        year INTEGER
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# Pydantic model
class Book(BaseModel):
    title: str
    author: str
    genre: str
    year: int

# Routes
@app.post("/books/")
def create_book(book: Book):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)",
                   (book.title, book.author, book.genre, book.year))
    conn.commit()
    conn.close()
    return {"message": "Book added successfully"}

@app.get("/books/", response_model=List[Book])
def get_books(genre: Optional[str] = None, author: Optional[str] = None):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    if genre:
        query += " AND genre=?"
        params.append(genre)
    if author:
        query += " AND author=?"
        params.append(author)
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [{"title": row[1], "author": row[2], "genre": row[3], "year": row[4]} for row in rows]

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=?, genre=?, year=? WHERE id=?",
                   (book.title, book.author, book.genre, book.year, book_id))
    conn.commit()
    conn.close()
    return {"message": "Book updated successfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()
    return {"message": "Book deleted successfully"}
