"""
Books API client with specific endpoints.
"""

import os
from typing import Dict, Any, List, Optional
import requests
from src.api.base_client import BaseClient
from src.models.book_model import BookModel


class BooksClient(BaseClient):
    """
    Client for Books API endpoints.
    """

    def __init__(self, base_url: str = os.getenv("BOOKS_API_BASE_URL")):
        """
        Initialize Books API client.
        """
        super().__init__(base_url)
        self.books_endpoint = (
            f"/api/{os.getenv("API_VERSION")}/{os.getenv("BOOKS_API_ENDPOINT")}"
        )
        pass

    def get_all_books(self) -> requests.Response:
        """
        Get all books.

        """
        return self.get(self.books_endpoint)

    def get_book_by_id(self, book_id: int) -> requests.Response:
        """
        Get book by ID.

        """
        return self.get(f"{self.books_endpoint}/{book_id}")

    def create_book(self, book_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new book.

        """
        return self.post(self.books_endpoint, data=book_data)

    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> requests.Response:
        """
        Update existing book.

        Args:
            book_id: Book ID to update
            book_data: Updated book data
        """
        return self.put(f"{self.books_endpoint}/{book_id}", data=book_data)

    def delete_book(self, book_id: int) -> requests.Response:
        """
        Delete book by ID.

        Args:
            book_id: Book ID to delete
        """
        return self.delete(f"{self.books_endpoint}/{book_id}")

    # TODO: Is this needed?????

    def create_book_from_model(self, book: BookModel) -> requests.Response:
        """
        Create book from Book model.

        Args:
            book: Book model instance

        """
        return self.create_book(book.to_dict())

    def update_book_from_model(
        self, book_id: int, book: BookModel
    ) -> requests.Response:
        """
        Update book from Book model.

        Args:
            book_id: Book ID to update
            book: Book model instance

        """
        return self.update_book(book_id, book.to_dict())
