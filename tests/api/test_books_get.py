"""
Tests for Books API - GET endpoints.
"""

import pytest
from src.api.books_client import BooksClient


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
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

        books_data = response.json()
        assert isinstance(books_data, list)

    def test_response_books_structure(self, books_api_client: BooksClient) -> None:
        """
        Test structure of books in the response.
        Edge case: Validate that each book in the list has expected fields.
        """
        # Act
        response = books_api_client.get_all_books()
        books_data = response.json()

        # Validate each book structure if books exist
        assert response.status_code == 200

        # TODO: Test structure of each book in the list based on expected schema
        assert isinstance(books_data, list)

    def test_get_all_books_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting all books is reasonable.
        """
        # Act & Assert
        response = books_api_client.get_all_books()

        # Response should be under 5 seconds for good performance
        assert response.elapsed.total_seconds() < 5.0
        assert response.status_code == 200


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
        # Act
        response = books_api_client.get_book_by_id(book_id)

        # Assert
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        assert response.json() is not None

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

        assert response.status_code in [404, 400]

        # TODO: Validate error response structure
        # assert ResponseValidator.validate_error_response(response)

    @pytest.mark.parametrize("invalid_id_type", ["abc", "12.5", "null", "undefined"])
    def test_get_book_by_invalid_id_type(
        self, books_api_client: BooksClient, invalid_id_type: str
    ) -> None:
        """
        Test retrieval with invalid ID types.

        Edge case: API should handle non-integer IDs.
        """
        # Act
        response = books_api_client.get(f"/api/v1/Books/{invalid_id_type}")

        # Assert
        assert response.status_code in [400, 404]

        # TODO: Validate error response structure
        # assert ResponseValidator.validate_error_response(response)

    def test_get_book_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting single book.
        """
        # Act
        response = books_api_client.get_book_by_id(1)

        # Assert
        assert response.elapsed.total_seconds() < 3.0
        assert response.status_code == 200
