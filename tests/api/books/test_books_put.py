"""
Tests for Books API - PUT endpoints.
"""

import pytest
from src.clients.books_client import BooksClient
from src.data.books_data import BooksData
from src.models.books_models import BookModels
from src.utils.validators import (
    validate_content_type,
    validate_json_data,
    validate_json_schema,
    validate_response_reason,
    validate_status_code,
)


@pytest.mark.api
class TestPutBooks:
    """
    Test suite for PUT /api/v1/Books/{id} endpoint.
    """

    def test_put_existing_book_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful update of existing book.

        Sunny day scenario: API returns 200 status with updated book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data
        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)

        book_id = test_book_data["id"]
        updated_book_data = BooksData.updated_book_data.copy()
        updated_book_data["id"] = book_id

        # Act
        put_response = books_api_client.update_book(book_id, updated_book_data)

        # Assert
        validate_status_code(put_response, 200)
        validate_content_type(put_response, "application/json")
        validate_response_reason(put_response, "OK")

        put_response_json = put_response.json()
        validate_json_schema(put_response_json, BookModels.book_response_model)
        validate_json_data(put_response_json, updated_book_data)

    @pytest.mark.parametrize(
        "book_id",
        [-1, 0, 1, 2, 3, 99, 100, 199, 200, 201, 500, 1762, 99999, 10900],
    )
    def test_put_book_with_parametrized_id(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test updating book with a parametrized ID, validate by GET.

        Sunny day scenario: API returns 200 status with updated book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data.copy()
        test_book_data["id"] = book_id

        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)

        updated_book_data = BooksData.updated_book_data.copy()
        updated_book_data["id"] = book_id

        # Act
        put_response = books_api_client.update_book(book_id, updated_book_data)

        # Assert
        validate_status_code(put_response, 200)
        validate_content_type(put_response, "application/json")
        put_response_json = put_response.json()
        validate_json_schema(put_response_json, BookModels.book_response_model)
        validate_json_data(put_response_json, updated_book_data)

        get_book_response = books_api_client.get_book_by_id(book_id)
        validate_status_code(get_book_response, 200)
        validate_content_type(get_book_response, "application/json")
        get_book_response_json = get_book_response.json()
        validate_json_schema(get_book_response_json, BookModels.book_response_model)
        validate_json_data(get_book_response_json, updated_book_data)

    def test_put_book_with_invalid_data(self, books_api_client: BooksClient) -> None:
        """
        Test updating book with invalid data.
        Asumption: API should return 400 Bad Request for invalid data.

        Edge case: API should handle invalid data gracefully.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data.copy()
        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)

        book_id = test_book_data["id"]
        invalid_book_data = BooksData.invalid_book_data.copy()
        invalid_book_data["id"] = str(book_id)
        invalid_book_data["pageCount"] = str(-1000)

        # Act
        put_response = books_api_client.update_book(book_id, invalid_book_data)

        # Assert
        validate_status_code(put_response, 400)
        validate_content_type(put_response, "application/problem+json")
        validate_response_reason(put_response, "Bad Request")
