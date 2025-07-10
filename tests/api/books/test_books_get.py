"""
Tests for Books API - GET endpoints.
"""

import pytest
from src.clients.books_client import BooksClient
from src.models.books_models import BookModels
from src.utils.validators import (
    validate_content_type,
    validate_elapsed_time,
    validate_json_schema,
    validate_status_code,
)


@pytest.mark.api
class TestGetBooks:
    """
    Test suite for GET /api/v1/Books endpoint.
    """

    @pytest.mark.smoke
    def test_get_all_books_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful retrieval of all books.

        Sunny day scenario: API returns list of books with 200 status.
        """

        # Act
        response = books_api_client.get_all_books()

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")

        books_data = response.json()

        for book in books_data:
            validate_json_schema(book, BookModels.book_response_model)

    def test_get_all_books_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting all books is reasonable.

        Edge case: Ensure API responds quickly for performance.
        """

        # Act
        response = books_api_client.get_all_books()

        # Assert
        validate_status_code(response, 200)
        validate_elapsed_time(response, 5.0)


@pytest.mark.api
class TestGetBookById:
    """
    Test suite for GET /api/v1/Books/{id} endpoint.
    """

    @pytest.mark.parametrize("book_id", [1, 5, 10, 50, 100])
    def test_get_book_by_valid_id_success(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test successful retrieval of book by valid ID.

        Sunny day scenario: API returns specific book with 200 status.
        """
        # Act
        response = books_api_client.get_book_by_id(book_id)

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")

        book = response.json()
        validate_json_schema(book, BookModels.book_response_model)

    @pytest.mark.parametrize("invalid_id", [0, -1, -100, 999999, 1000000])
    def test_get_book_by_invalid_id(
        self, books_api_client: BooksClient, invalid_id: int
    ) -> None:
        """
        Test retrieval of book with invalid/non-existent ID.

        Edge case: API should handle invalid IDs gracefully.
        """

        # Act
        response = books_api_client.get_book_by_id(invalid_id)

        # Assert
        validate_status_code(response, 404)
        validate_content_type(response, "application/problem+json")

        problem_json = response.json()
        validate_json_schema(problem_json, BookModels.book_not_found_response_model)

    @pytest.mark.parametrize("invalid_id_type", ["abc", "12.5", "null", "undefined"])
    def test_get_book_by_invalid_id_type(
        self, books_api_client: BooksClient, invalid_id_type: str
    ) -> None:
        """
        Test retrieval with invalid ID types.

        Edge case: API should handle non-integer IDs.
        """

        # Act
        response = books_api_client.get_book_by_id(invalid_id_type)

        # Assert
        validate_status_code(response, 400)
        validate_content_type(response, "application/problem+json")

        problem_json = response.json()
        validate_json_schema(problem_json, BookModels.book_not_found_response_model)

    def test_get_book_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting single book.

        Edge case: Ensure API responds quickly for performance.
        """

        # Act
        get_response = books_api_client.get_book_by_id(1)

        # Assert
        validate_status_code(get_response, 200)
        validate_elapsed_time(get_response, 5.0)
