"""
Tests for Books API - DELETE endpoints.
"""

import pytest

from src.clients.books_client import BooksClient
from src.data.books_data import BooksData
from src.models.books_models import BookModels
from src.utils.validators import (
    validate_json_schema,
    validate_response_reason,
    validate_status_code,
)


@pytest.mark.api
class TestDeleteBooks:
    """
    Test suite for DELETE /api/v1/Books/{id} endpoint.
    """

    def test_delete_existing_book_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful deletion of book which exists.

        Sunny day scenario: API returns 200 status with deleted book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data
        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)
        book_id = test_book_data["id"]

        # Act
        delete_response = books_api_client.delete_book(book_id)

        # Assert
        validate_status_code(delete_response, 200)
        validate_response_reason(delete_response, "OK")

        get_book_response = books_api_client.get_book_by_id(book_id)
        validate_status_code(get_book_response, [400, 404])
        validate_response_reason(get_book_response, "Not Found")

        get_book_response_json = get_book_response.json()

        validate_json_schema(
            get_book_response_json, BookModels.book_not_found_response_model
        )

    @pytest.mark.parametrize("book_id", [-1, 0, 666, 500, 1762])
    def test_delete_non_existing_book(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test deletion of book which does not exist.

        Edge case: API returns 404 status with error message.
        """

        # Arrange
        get_response = books_api_client.get_book_by_id(book_id)
        validate_status_code(get_response, 404)
        validate_response_reason(get_response, "Not Found")

        # Act
        delete_response = books_api_client.delete_book(book_id)

        # Assert
        validate_status_code(delete_response, 200)
        validate_response_reason(delete_response, "OK")
