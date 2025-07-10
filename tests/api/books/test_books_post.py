"""
Tests for Books API - POST endpoints.
"""

import pytest
from jsonschema import validate
from src.clients.books_client import BooksClient
from src.data.books_data import BooksData
from src.models.books_models import BookModels


@pytest.mark.api
class TestPostBooks:
    """
    Test suite for POST /api/v1/Books endpoint.
    """

    @pytest.mark.smoke
    def test_post_book_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful creation of book.

        Sunny day scenario: API returns 200 status with created book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data

        # Act
        post_response = books_api_client.create_book(test_book_data)

        # Assert
        assert post_response.status_code == 200
        assert "application/json" in post_response.headers.get("content-type", "")
        post_book_response = post_response.json()

        validate(post_book_response, BookModels.book_response_model)

        assert isinstance(post_book_response["id"], int)
        assert post_book_response["title"] == test_book_data["title"]
        assert post_book_response["description"] == test_book_data["description"]
        assert post_book_response["pageCount"] == test_book_data["pageCount"]
        assert post_book_response["excerpt"] == test_book_data["excerpt"]
        assert post_book_response["publishDate"] == test_book_data["publishDate"]

    def test_post_book_invalid_data(self, books_api_client: BooksClient) -> None:
        """
        Test creation of book with invalid data.

        Edge case: API should return 400 Bad Request for invalid input.
        """

        # Arrange
        invalid_book_data = BooksData.invalid_book_data

        # Act
        response = books_api_client.create_book(invalid_book_data)

        # Assert
        assert response.status_code == 400
        assert "application/json" in response.headers.get("content-type", "")
        error_response = response.json()

        validate(error_response, BookModels.book_not_found_response_model)

    def test_post_book_missing_required_fields(
        self, books_api_client: BooksClient
    ) -> None:
        """
        Test creation of book with missing required fields.

        Edge case: API should return 400 Bad Request for missing fields.
        """

    def test_post_book_with_parametrized_invalid_fields(
        self, books_api_client: BooksClient
    ) -> None:
        """
        Test creation of book with invalid fields not defined in schema.

        Edge case: API should ignore extra fields and return valid book data.
        """
