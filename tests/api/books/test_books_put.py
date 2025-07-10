"""
Tests for Books API - PUT endpoints.
"""

import pytest
from src.clients.books_client import BooksClient
from src.data.books_data import BooksData
from src.models.books_models import BookModels
from src.utils.validators import (
    validate_content_type,
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

        # Verify the book was actually updated
        assert put_response_json["id"] == book_id
        assert put_response_json["title"] == updated_book_data["title"]
        assert put_response_json["description"] == updated_book_data["description"]
        assert put_response_json["pageCount"] == updated_book_data["pageCount"]
        assert put_response_json["excerpt"] == updated_book_data["excerpt"]
        assert put_response_json["publishDate"] == updated_book_data["publishDate"]

    def test_put_nonexistent_book_failure(self, books_api_client: BooksClient) -> None:
        """
        Test updating nonexistent book fails appropriately.

        Edge case: API should return 404 for non-existent book ID.
        """

        # Arrange
        nonexistent_book_id = 999999
        updated_book_data = BooksData.updated_book_data.copy()
        updated_book_data["id"] = nonexistent_book_id

        # Act
        put_response = books_api_client.update_book(
            nonexistent_book_id, updated_book_data
        )

        # Assert
        validate_status_code(put_response, 404)
        validate_response_reason(put_response, "Not Found")

        put_response_json = put_response.json()
        validate_json_schema(
            put_response_json, BookModels.book_not_found_response_model
        )

    def test_put_book_with_invalid_data(self, books_api_client: BooksClient) -> None:
        """
        Test updating book with invalid data.

        Edge case: API should handle invalid data gracefully.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data
        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)

        book_id = test_book_data["id"]
        invalid_book_data = BooksData.invalid_book_data.copy()
        invalid_book_data["id"] = str(book_id)

        # Act
        put_response = books_api_client.update_book(book_id, invalid_book_data)

        # Assert
        # Note: The API behavior with invalid data may vary
        # This test documents the current behavior
        validate_status_code(put_response, [200, 400])

        if put_response.status_code == 200:
            put_response_json = put_response.json()
            validate_json_schema(put_response_json, BookModels.book_response_model)
        elif put_response.status_code == 400:
            validate_response_reason(put_response, "Bad Request")

    @pytest.mark.parametrize("book_id", [1, 5, 10, 50, 100, 200])
    def test_put_book_parametrized_ids(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test updating books with different valid book IDs.

        Parametrized test: Verify PUT works with various book IDs.
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

        # Verify the update was successful
        assert put_response_json["id"] == book_id
        assert put_response_json["title"] == updated_book_data["title"]
        assert put_response_json["pageCount"] == updated_book_data["pageCount"]
