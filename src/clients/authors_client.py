"""
Authors API client with specific endpoints.
"""

import os
from typing import Dict, Any
import requests
from src.clients.base_client import BaseClient


class AuthorsClient(BaseClient):
    """
    Client for Authors API endpoints.
    """

    def __init__(self) -> None:
        """
        Initialize Authors API client.
        """
        super().__init__()
        self.authors_endpoint = (
            f"/api/{os.getenv('API_VERSION')}/{os.getenv('AUTHORS_API_ENDPOINT')}"
        )

    def get_all_authors(self) -> requests.Response:
        """
        Get all authors.

        GET /api/v1/Authors – Retrieve a list of all authors.

        Returns:
            HTTP response object
        """
        return self.get(self.authors_endpoint)

    def get_author_by_id(self, author_id: int | str) -> requests.Response:
        """
        Get author by ID.

        GET /api/v1/Authors/{id} – Retrieve details of a specific author by their ID.

        Args:
            author_id: Author ID to retrieve

        Returns:
            HTTP response object
        """
        return self.get(f"{self.authors_endpoint}/{author_id}")

    def create_author(self, author_data: Dict[str, Any]) -> requests.Response:
        """
        Create a new author.

        POST /api/v1/Authors – Add a new author to the system.

        Args:
            author_data: Author data dictionary

        Returns:
            HTTP response object
        """
        return self.post(self.authors_endpoint, data=author_data)

    def update_author(
        self, author_id: int | str, author_data: Dict[str, Any]
    ) -> requests.Response:
        """
        Update existing author.

        PUT /api/v1/Authors/{id} – Update an existing author's details.

        Args:
            author_id: Author ID to update
            author_data: Updated author data

        Returns:
            HTTP response object
        """
        return self.put(f"{self.authors_endpoint}/{author_id}", data=author_data)

    def delete_author(self, author_id: int) -> requests.Response:
        """
        Delete author by ID.

        DELETE /api/v1/Authors/{id} – Delete an author by their ID.

        Args:
            author_id: Author ID to delete

        Returns:
            HTTP response object
        """
        return self.delete(f"{self.authors_endpoint}/{author_id}")

    def get_authors_by_book_id(self, book_id: int | str) -> requests.Response:
        """
        Get authors by book ID.

        GET /api/v1/Authors/authors/books/{idBook} – Retrieve authors for a specific book.

        Args:
            book_id: Book ID to get authors for

        Returns:
            HTTP response object
        """
        return self.get(f"{self.authors_endpoint}/authors/books/{book_id}")
