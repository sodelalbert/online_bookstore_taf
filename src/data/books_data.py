"""
Book Data Class for API Tests
"""

from dataclasses import dataclass


@dataclass
class BooksData:
    """
    Data class for book data used in API tests.
    """

    sample_book_data = {
        "id": 1,
        "title": "Test Book",
        "description": "This is a test book.",
        "pageCount": 300,
        "excerpt": "An excerpt from the test book.",
        "publishDate": "2023-10-01T00:00:00Z",
    }

    updated_book_data = {
        "title": "Updated Test Book",
        "description": "This is an updated test book.",
        "pageCount": 350,
        "excerpt": "An updated excerpt from the test book.",
        "publishDate": "2025-11-01T00:00:00Z",
    }

    invalid_book_data = {
        "id": None,
        "title": "",
        "description": "",
        "pageCount": None,
        "excerpt": "",
        "publishDate": "2025-11-01T00:00:00Z",
    }
