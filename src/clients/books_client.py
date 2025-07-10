"""
Books API client with specific endpoints.
"""

import os
from typing import Dict, Any
import requests
from src.clients.base_client import BaseClient


class BooksClient(BaseClient):
    """
    Client for Books API endpoints.
    """

    def __init__(self) -> None:
        """
        Initialize Books API client.
        """
        super().__init__()
        self.books_endpoint = (
            f"/api/{os.getenv("API_VERSION")}/{os.getenv("BOOKS_API_ENDPOINT")}"
        )

    def get_all_books(self) -> requests.Response:
        """
        Get all books.

        """
        return self.get(self.books_endpoint)

    def get_book_by_id(self, book_id: int | str) -> requests.Response:
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
