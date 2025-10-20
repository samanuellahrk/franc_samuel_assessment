#!/usr/bin/env python3
"""
Bookstore Client

A client application for interacting with the Bookstore API.
This client is intentionally incomplete and contains TODOs for implementation.
"""
import requests
import json
from tabulate import tabulate
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
API_BASE_URL = "http://localhost:5000/api"
BOOKS_ENDPOINT = f"{API_BASE_URL}/books"
REQUESTS_TIMEOUT = 5  # seconds, adjust as needed


# Helper functions
def safe_get_json(response):
    """
    Return parsed JSON or None and log an error.
    
    Helps return safe error instead of crashing on invalid JSON responses.
    """
    try:
        return response.json()
    except json.JSONDecodeError:
        print_error("Server returned invalid JSON.")
        return None
    
def print_success(message):
    """Print a success message in green."""
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    """Print an error message in red."""
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

def print_info(message):
    """Print an info message in blue."""
    print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")

def format_book_table(books):
    """Format a list of books as a table."""
    if not books:
        return "No books found."
    
    # Convert single book to list if needed
    if isinstance(books, dict):
        books = [books]
    
    headers = ["ID", "Title", "Author", "Price", "In Stock"]
    rows = [
        [
            book.get("id", "N/A"),
            book.get("title", "N/A"),
            book.get("author", "N/A"),
            f"${book.get('price', 0):.2f}",
            "Yes" if book.get("in_stock", False) else "No"
        ]
        for book in books
    ]
    
    return tabulate(rows, headers=headers, tablefmt="grid")

# API client functions

def get_all_books():
    """
    Retrieve all books from the API.
    """
    try:
        response = requests.get(BOOKS_ENDPOINT, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        books = safe_get_json(response)
        return books
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to retrieve books: {e}")
        return []

def display_all_books():
    """
    Display all books in a formatted table.
    """
    print_info("Fetching all books...")
    # fecthes and displays all books
    books = get_all_books()
    print(format_book_table(books))

def get_book_by_id(book_id):
    """
    Retrieve a specific book by ID.
    
    Parameters:
        book_id (str): The ID of the book to retrieve
        
    Returns:
        dict: The book data if found, None otherwise
    """
    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/{book_id}", timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        book = safe_get_json(response)
        return book # returns book data
    
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to retrieve book {book_id}: {e}")
        return None
    pass

def display_book_details():
    """
    Display details for a specific book.
    """
    # prompts user for non-empty book ID
    while True:
        book_id = input("Enter book ID: ").strip()
        if book_id:
            break
        print_error("ID cannot be empty. Please try again.")
    
    # retrieves and displays book details, if book ID is found
    book = get_book_by_id(book_id)
    if book:
        print(format_book_table(book))
    else:
        print_error(f"Book with ID {book_id} not found or could not be retrieved.")

def add_book():
    """
    Add a new book to the bookstore.
    
    Gather book details from the user and send them to the API.
    """    
    title, author, price, in_stock = None, None, None, None

    # Prompt user for book details with validation

    # book title
    while True:
        title = input("Enter book title: ").strip()
        if title:
            break
        print_error("Title cannot be empty. Please try again.")
    # book author
    while True:
        author = input("Enter book author: ").strip()
        if author:
            break
        print_error("Author cannot be empty. Please try again.")
    # book price
    while True:
        price_input = input("Enter book price: ").strip()
        try:
            price = float(price_input)
            if price < 0:
                raise ValueError
            break
        except ValueError:
            print_error("Price must be a non-negative number. Please try again.")
    # book availability
    while True:
        in_stock_input = input("Is the book in stock? (y/n): ").strip().lower()
        if in_stock_input == 'y':
            in_stock = True
            break
        elif in_stock_input == 'n':
            in_stock = False
            break
        print_error("Please enter 'y' for yes or 'n' for no.")
    
    book_data = {
        "title": title,
        "author": author,
        "price": price,
        "in_stock": in_stock
    }
    # POST request to add the new book
    try:
        response = requests.post(BOOKS_ENDPOINT, json=book_data, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        print_success("Book added successfully!")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to add book: {e}")
        return
        

def update_book():
    """
    Update an existing book's information.
    
    Retrieve the current book information and allow the user to modify it.
    """

    # Prompts user to update book by ID with validation
    while True:
        book_id = input("Enter the book ID to update: ").strip()
        if not book_id:
            print_error("Book ID cannot be empty. Please try again.")
            continue

        book = get_book_by_id(book_id)
        if not book:
            print_error(f"Book with ID {book_id} not found or could not be retrieved. Please try again.")
            continue

        break

    # Title
    print_info("Leave field empty to keep current value.")
    print(f"Current Title: {book['title']}")
    new_title = input("New Title: ").strip()
    if not new_title:
        new_title = book['title']

    # Author
    print(f"Current Author: {book['author']}")
    new_author = input("New Author: ").strip()
    if not new_author:
        new_author = book['author']

    # Price
    print(f"Current Price: ${book['price']:.2f}")
    while True:
        new_price_input = input("New Price: ").strip()
        if not new_price_input:
            new_price = book['price']
            break
        try:
            new_price = float(new_price_input)
            if new_price < 0:
                raise ValueError
            break
        except ValueError:
            print_error("Price must be a non-negative number. Please try again.")

    # Availability
    print(f"Current In Stock: {'Yes' if book.get('in_stock', False) else 'No'}")
    while True:
        new_in_stock_input = input("Is the book in stock? (y/n): ").strip().lower()
        if not new_in_stock_input:
            new_in_stock = book.get('in_stock', False)
            break
        elif new_in_stock_input == 'y':
            new_in_stock = True
            break
        elif new_in_stock_input == 'n':
            new_in_stock = False
            break
        print_error("Please enter 'y' for yes or 'n' for no, or leave empty to keep current value.")

    updated_book = {
        "title": new_title,
        "author": new_author,
        "price": new_price,
        "in_stock": new_in_stock
    }
    # PUT request to update the book
    try:
        response = requests.put(f"{BOOKS_ENDPOINT}/{book_id}", json=updated_book, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        print_success("Book updated successfully!")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to update book: {e}")

def delete_book():
    """
    Delete a book from the bookstore.
    
    Ask for confirmation before deleting.
    """

    # Prompts user to delete book by ID with validation
    while True:
        book_id = input("Enter the book ID to delete: ").strip()
        if not book_id:
            print_error("Book ID cannot be empty. Please try again.")
            continue

        book = get_book_by_id(book_id)
        if not book:
            print_error(f"Book with ID {book_id} not found or could not be retrieved. Please try again.")
            continue

        break
    # Confirm deletion
    print_info(f"Selected Book:\n{format_book_table(book)}")
    confirm = input("Are you sure you want to delete this book? (y/n): ").strip().lower()
    if confirm != 'y':
        print_info("Delete operation cancelled.")
        return
    # DELETE request to remove the book
    try:
        response = requests.delete(f"{BOOKS_ENDPOINT}/{book_id}", timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        print_success(f"Book with ID {book_id} deleted successfully!")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to delete book: {e}")

def search_books():
    """
    Search for books by title or author.
    
    Send a search query to the API and display the results.
    """

    # Prompt user for search query with validation
    while True:
        query = input("Enter search query (title or author): ").strip()
        if query:
            break
        print_error("Search query cannot be empty.")
            
    # GET request to search for books
    try:
        response = requests.get(f"{BOOKS_ENDPOINT}/search", params={"query": query}, timeout=REQUESTS_TIMEOUT)
        response.raise_for_status()
        books = safe_get_json(response)
        # Display results
        if books:
            print_success(f"Found {len(books)} book(s) matching '{query}':")
            print(format_book_table(books))
        else:
            print_info("No books found matching your query.")
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to search books: {e}")

def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("             BOOKSTORE CLIENT              ")
    print("=" * 50)
    print("1. View All Books")
    print("2. View Book Details")
    print("3. Add New Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Search Books")
    print("7. Exit")
    print("=" * 50)

def main():
    """Main application function."""
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-7): ")
            
            if choice == "1":
                display_all_books()
            elif choice == "2":
                display_book_details()
            elif choice == "3":
                add_book()
            elif choice == "4":
                update_book()
            elif choice == "5":
                delete_book()
            elif choice == "6":
                search_books()
            elif choice == "7":
                print_info("Exiting Bookstore Client. Goodbye!")
                break
            else:
                print_error("Invalid choice. Please enter a number between 1 and 7.")
            
            input("\nPress Enter to continue...")
            
    except KeyboardInterrupt:
        print_info("\nApplication terminated by user.")
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 