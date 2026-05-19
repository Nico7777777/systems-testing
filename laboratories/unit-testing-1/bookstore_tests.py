import pytest

from bookstore.book import Book
from bookstore.book_repository import InMemoryBookRepository
from bookstore.services.book_filtering_service import BookFilterService
from bookstore.services.bookstore_service import BookStoreService


# TODO: Create a fixture that returns a BookService instance
def create_book_service():
    """
    INSTRUCTIONS:
    - Create and return a BookService instance
    - Use InMemoryBookRepository for storage
    - Use default BookFilterService
    
    HINTS:
    repository = ...
    book_filter_service = ...
    return BookService(repository, book_filter_service)
    """
    repo = InMemoryBookRepository()
    book_filter_service = BookFilterService()
    inst = BookStoreService(repo, book_filter_service)
    return inst

# TODO: Create a fixture that returns a sample book for testing
def create_sample_book():
    """
    INSTRUCTIONS:
    - Create a Book instance with sample data
    - Use realistic values for title, author, genre, and price
    
    REQUIREMENTS:
    - Book should have valid, testable attributes
    """
    b = Book(title="Mogley", author="J.K. Rowling", genre="SF", price=13.44)
    return b


# INFO: For the following tests, use only the BookService instance created by the fixture
def test_add_book():
    """
    TESTING OBJECTIVES:
    1. Create a book service using the fixture
    2. Create a sample book using the fixture
    3. Add the book to the service
    4. Verify:
       - Book has a non-None ID
       - Book attributes match the original book
    
    HINTS:
    - Use assertions to check book details
    - Verify ID is automatically assigned
    """
    # Your implementation here
    new_book_service = create_book_service()
    new_book = create_sample_book()
    new_book_service.add_book(new_book)
    assert new_book.id is not None
    assert new_book_service.get_book_by_id(new_book.id) == new_book


def test_add_book_validation():
    """
    TESTING OBJECTIVES:
    1. Attempt to add a book with invalid data
    2. Verify appropriate exception is raised
    
    REQUIREMENTS:
    - Test scenarios like:
      * Book with empty title
      * Book with empty author
    
    HINTS:
    - Use pytest.raises() to check for exceptions
    """
    # Your implementation here
    # with pytest.raises():
    new_book_service = create_book_service()
    with pytest.raises(ValueError):
        empty_title_b = Book(title="", author="J.K. Rowling", genre="SF", price=13.44)
        new_book_service.add_book(empty_title_b)
    with pytest.raises(ValueError):
        empty_author_b = Book(title="Mogley", author="", genre="SF", price=13.49)
        new_book_service.add_book(empty_author_b)

# INFO: Here you should use @pytest.mark.parametrize to test multiple genres
@pytest.mark.parametrize("genre, length", [("SF", 4), ("drama", 2)])
def test_get_books_by_genre(genre, length):
    """
    TESTING OBJECTIVES:
    1. Add multiple books with different genres
    2. Filter books by specific genres
    3. Verify:
       - Only books of the specified genre are returned
       - Filtering is case-insensitive
    
    REQUIREMENTS:
    - Add books across multiple genres
    - Test filtering with different genre inputs
    
    HINTS:
    - Use service's get_books() method with genre parameter
    - Check length and genre of returned books
    """
    # Your implementation here
    new_book_service = create_book_service()

    book1 = Book(title="Mogley", author="J.K. Rowling", genre="SF", price=13.44)
    book2 = Book(title="Spider Man", author="Marvel", genre="SF", price=16.50)
    book3 = Book(title="Lord of the rings", author="J.R.R.T.", genre="SF", price=12.99)
    book4 = Book(title="si maine e o zi...", author="R. Diana", genre="drama", price=17.34)
    book5 = Book(title="Learn how to love again", author="Martin Luthor", genre="drama", price=16.79)
    book6 = Book(title="Game of Thrones", author="G.R.R.M.", genre="SF", price=16.98)

    new_book_service.add_book(book1)
    new_book_service.add_book(book2)
    new_book_service.add_book(book3)
    new_book_service.add_book(book4)
    new_book_service.add_book(book5)
    new_book_service.add_book(book6)

    SFs = new_book_service.get_books(genre=genre)
    assert len(SFs) == length

    # dramas = new_book_service.get_books(genre="drama")
    # assert len(dramas) == 2
    
# INFO: Here you should use @pytest.mark.parametrize to test multiple price ranges
@pytest.mark.parametrize("range, output", [((13, 14), 1), ((16.50, 17.50), 4), ((16.70, 16.99), 2)])
def test_price_range_filtering(range: tuple, output):
    """
    TESTING OBJECTIVES:
    1. Add books at different price points
    2. Test filtering by:
       - Minimum price
       - Maximum price
       - Combined price range
    
    REQUIREMENTS:
    - Verify correct number of books returned
    - Ensure only books within price range are included
    
    HINTS:
    - Add books with varied prices
    - Use get_books() with min_price and max_price
    - Test edge cases and different price combinations
    """
    # Your implementation here
    new_book_service = create_book_service()

    book1 = Book(title="Mogley", author="J.K. Rowling", genre="SF", price=13.44)
    book2 = Book(title="Spider Man", author="Marvel", genre="SF", price=16.50)
    book3 = Book(title="Lord of the rings", author="J.R.R.T.", genre="SF", price=12.99)
    book4 = Book(title="si maine e o zi...", author="R. Diana", genre="drama", price=17.34)
    book5 = Book(title="Learn how to love again", author="Martin Luthor", genre="drama", price=16.79)
    book6 = Book(title="Game of Thrones", author="G.R.R.M.", genre="SF", price=16.98)

    new_book_service.add_book(book1)
    new_book_service.add_book(book2)
    new_book_service.add_book(book3)
    new_book_service.add_book(book4)
    new_book_service.add_book(book5)
    new_book_service.add_book(book6)

    list_of_books = new_book_service.get_books(min_price=range[0], max_price=range[1])
    assert len(list_of_books) == output

def test_update_book():
    """
    TESTING OBJECTIVES:
    1. Add a book to the service
    2. Update the book's details
    3. Verify:
       - Specific attributes can be updated
       - Updated values are correct
       - Other attributes remain unchanged
    
    REQUIREMENTS:
    - Test updating multiple attributes
    - Ensure update works for different book properties
    
    HINTS:
    - Use update_book() method
    - Compare book before and after update
    """
    # Your implementation here
    new_book_service = create_book_service()
    book1 = Book(title="Mogley", author="J.K. Rowling", genre="SF", price=13.44)
    new_book_service.add_book(book1)

    book1.genre = "drama"
    assert book1.genre == "drama"
    assert book1.price == 13.44
    assert book1.title == "Mogley"

    book1.author = "Mickey Mouse"
    assert book1.author == "Mickey Mouse"
    assert book1.price == 13.44
    assert book1.title == "Mogley"

def test_remove_book():
    """
    TESTING OBJECTIVES:
    1. Add a book to the service
    2. Remove the book
    3. Verify:
       - Book is successfully removed
       - Attempting to retrieve the book returns None
    
    REQUIREMENTS:
    - Test successful book removal
    - Test removing a non-existent book
    
    HINTS:
    - Use remove_book() method
    - Check return value of remove operation
    - Verify book is no longer in the service
    """
    # Your implementation here
    new_book_service = create_book_service()
    book1 = Book(title="Mogley", author="J.K. Rowling", genre="SF", price=13.44)
    new_book_service.add_book(book1)

    new_book_service.remove_book(book1.id)
    assert len(new_book_service.get_books()) == 0
    assert new_book_service.get_book_by_id(book1.id) == None
