# Bookstore Client

A Python client application for interacting with a Bookstore API.  
This client allows users to view, add, update, delete, and search for books in a bookstore.

---

## Features / Functionalities

- **List all books**: Retrieve and display all books from the API in a nicely formatted table.
- **View book details**: Get details for a specific book by its ID.
- **Add a new book**: Input book information (title, author, price, in-stock status) and add it to the API.
- **Update an existing book**: Modify a book's details by ID.
- **Delete a book**: Remove a book from the API with confirmation.
- **Search books**: Find books by title or author.

**Error Handling**:

- Handles API/network errors gracefully and prints user-friendly error messages.
- Validates user input to prevent invalid requests.

---

## Requirements

- Python 3.12+
- Libraries:
  - `requests`
  - `tabulate`
  - `colorama`

You can install dependencies via:

```bash
pip install -r requirements.txt
```

## Usage

First run the Bookstore API service:
```bash
python bookstore_api/app.py
```

Then, run the client application:

```bash
python bookstore_client/client.py
```

The application will present a menu of options to interact with the bookstore:
```bash
1. View All Books
2. View Book Details
3. Add New Book
4. Update Book
5. Delete Book
6. Search Books
7. Exit
Select an option (1-7):
```

You can interact with the bookstore by entering the corresponding number for each action.

---

## Testing
There is a test file available at `bookstore_client/test_client.py` which includes unit tests for the client functionalities. You can run the tests using:

```bash
python -m pytest bookstore_client/test_client.py -v    
```

---