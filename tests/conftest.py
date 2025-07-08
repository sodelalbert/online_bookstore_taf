"""
Global pytest configuration and fixtures.
"""

from typing import Generator, List
import pytest
from src.api.books_client import BooksClient
from src.utils.data_factory import BookDataFactory


@pytest.fixture(scope="session")
def books_api_client() -> Generator[BooksClient, None, None]:
    """
    Create Books API client for testing.

    Yields:
        BooksAPIClient instance
    """
    client = BooksClient()
    yield client


# @pytest.fixture(scope="function")
# def sample_book_data() -> dict:
#     """
#     Provide sample book data for tests.

#     Returns:
#         Dictionary with sample book data
#     """
#     return BookDataFactory.create_valid_book_data(remove_id=True)


# @pytest.fixture(scope="function")
# def book_data_factory() -> type[BookDataFactory]:
#     """
#     Provide BookDataFactory for tests.

#     Returns:
#         BookDataFactory class
#     """
#     return BookDataFactory


# @pytest.fixture(scope="function")
# def cleanup_books() -> Generator[List[str], None, None]:
#     """Track created books for cleanup.

#     Yields:
#         List to track created book IDs
#     """
#     created_books: List[str] = []
#     yield created_books

#     # Cleanup logic could be added here if the API supported it
