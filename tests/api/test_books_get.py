"""
Tests for Books API - GET endpoints.
"""

import pytest
from jsonschema import validate
from src.api.books_client import BooksClient
from src.models.book_model import BookModel


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
        response = books_api_client.get_all_books()

        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

        books_data = response.json()

        assert isinstance(books_data, list)

        for book in books_data:
            validate(book, BookModel.book_response_schema)

    def test_get_all_books_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting all books is reasonable.
        Edge case: Ensure API responds quickly for performance.
        """

        response = books_api_client.get_all_books()

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 5.0


@pytest.mark.api
class TestGetBookById:
    """
    Test suite for GET /api/v1/Books/{id} endpoint.
    """

    @pytest.mark.smoke
    @pytest.mark.parametrize("book_id", [1, 5, 10, 50, 100])
    def test_get_book_by_valid_id_success(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test successful retrieval of book by valid ID.

        Sunny day scenario: API returns specific book with 200 status.
        """

        response = books_api_client.get_book_by_id(book_id)

        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

        book = response.json()
        validate(book, BookModel.book_response_schema)

    @pytest.mark.parametrize("invalid_id", [0, -1, -100, 999999, 1000000])
    def test_get_book_by_invalid_id(
        self, books_api_client: BooksClient, invalid_id: int
    ) -> None:
        """
        Test retrieval of book with invalid/non-existent ID.

        Edge case: API should handle invalid IDs gracefully.
        """

        response = books_api_client.get_book_by_id(invalid_id)

        assert response.status_code == 404
        assert "application/problem+json" in response.headers.get("content-type", "")

        problem_json = response.json()
        validate(problem_json, BookModel.book_not_found_response_schema)

    @pytest.mark.parametrize("invalid_id_type", ["abc", "12.5", "null", "undefined"])
    def test_get_book_by_invalid_id_type(
        self, books_api_client: BooksClient, invalid_id_type: str
    ) -> None:
        """
        Test retrieval with invalid ID types.

        Edge case: API should handle non-integer IDs.
        """

        response = books_api_client.get_book_by_id(invalid_id_type)

        assert response.status_code == 400

        problem_json = response.json()
        validate(problem_json, BookModel.book_not_found_response_schema)

    def test_get_book_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting single book.

        Edge case: Ensure API responds quickly for performance.
        """

        response = books_api_client.get_book_by_id(1)

        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 3.0
