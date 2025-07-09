"""
Book Data Module
"""

from dataclasses import dataclass


@dataclass
class BookData:
    """
    Data class for book data used in API tests.
    """

    sample_book_data = {
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
        "title": "",
        "description": "",
        "pageCount": -100,
        "excerpt": "",
        "publishDate": "2025-11-01T00:00:00Z",
    }
