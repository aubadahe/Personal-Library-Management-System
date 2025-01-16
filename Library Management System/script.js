const form = document.getElementById("book-form");
const booksList = document.getElementById("books-list");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value;
    const author = document.getElementById("author").value;
    const genre = document.getElementById("genre").value;
    const year = document.getElementById("year").value;

    // Send POST request to API
    await fetch("http://127.0.0.1:8000/books/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, author, genre, year: parseInt(year) }),
    });

    loadBooks();
    form.reset();
});

async function loadBooks() {
    const response = await fetch("http://127.0.0.1:8000/books/");
    const books = await response.json();
    booksList.innerHTML = books
        .map(
            (book) =>
                `<li><strong>${book.title}</strong> by ${book.author} (${book.year}) - ${book.genre}</li>`
        )
        .join("");
}

// Load books on page load
loadBooks();
