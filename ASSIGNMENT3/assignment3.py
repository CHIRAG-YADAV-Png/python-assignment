import json
from pathlib import Path

class Book:
    STATUS_AVAILABLE = "available"
    STATUS_ISSUED = "issued"
    
    def __init__(self, title, author, isbn, status=STATUS_AVAILABLE):
        self.title, self.author, self.isbn, self.status = title, author, isbn, status

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - Status: {self.status.capitalize()}"

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "status": self.status}

    def is_available(self):
        return self.status == self.STATUS_AVAILABLE

    def issue(self):
        if self.is_available():
            self.status = self.STATUS_ISSUED
            return True
        return False

    def return_book(self):
        self.status = self.STATUS_AVAILABLE
        return True

class LibraryInventory:
    def __init__(self, file_path="catalog.json"):
        self.file_path = Path(file_path)
        self.books = self._load_catalog()

    def _load_catalog(self):
        try:
            if not self.file_path.exists():
                return []
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book(**d) for d in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return [] 
        except Exception:
            return []

    def _save_catalog(self):
        try:
            data_to_save = [b.to_dict() for b in self.books]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
        except Exception as e:
            print(f"Error saving catalog: {e}")

    def add_book(self, book):
        if any(b.isbn == book.isbn for b in self.books):
            return False
        self.books.append(book)
        self._save_catalog()
        return True

    def search_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def search_by_title(self, query):
        q = query.lower()
        return [b for b in self.books if q in b.title.lower()]

    def display_all(self):
        return self.books

class CLI:
    def __init__(self):
        self.inventory = LibraryInventory()

    def display_menu(self):
        print("\n--- Library Manager ---")
        print("1. Add Book\n2. Issue Book\n3. Return Book\n4. View All\n5. Search\n6. Exit")
        print("-" * 25)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter choice: ").strip()

            try:
                if choice == '1':
                    title = input("Title: "); author = input("Author: "); isbn = input("ISBN: ")
                    if self.inventory.add_book(Book(title, author, isbn)):
                        print(f"Book '{title}' added.")
                    else:
                        print("Book with this ISBN already exists.")

                elif choice == '2':
                    isbn = input("ISBN to issue: ")
                    book = self.inventory.search_by_isbn(isbn)
                    if book and book.issue():
                        self.inventory._save_catalog()
                        print(f"Issued: {book.title}")
                    elif book:
                        print("Book is already issued.")
                    else:
                        print("Book not found.")

                elif choice == '3':
                    isbn = input("ISBN to return: ")
                    book = self.inventory.search_by_isbn(isbn)
                    if book:
                        book.return_book()
                        self.inventory._save_catalog()
                        print(f"Returned: {book.title}")
                    else:
                        print("Book not found.")

                elif choice == '4':
                    print("\n--- CATALOG ---")
                    for i, book in enumerate(self.inventory.display_all(), 1):
                        print(f"{i}. {book}")

                elif choice == '5':
                    query = input("Search Title or ISBN: ")
                    results = self.inventory.search_by_title(query) or ([self.inventory.search_by_isbn(query)] if self.inventory.search_by_isbn(query) else [])
                    print("\n--- RESULTS ---")
                    if results:
                        for book in results:
                            if book: print(book)
                    else:
                        print("No matches found.")

                elif choice == '6':
                    print("Exiting.")
                    break
                else:
                    print("Invalid choice.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    CLI().run()