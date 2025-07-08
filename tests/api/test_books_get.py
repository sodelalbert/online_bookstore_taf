"""
Tests for Books API - GET endpoints.
"""

import pytest
from src.api.books_client import BooksClient
from src.utils.validators import ResponseValidator


@pytest.mark.api
class TestGetBook:
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
        assert ResponseValidator.validate_content_type(response)
        assert ResponseValidator.validate_json_response(response)

        books_data = response.json()
        assert isinstance(books_data, list)

        # Validate each book structure if books exist
        if books_data:
            for book in books_data:
                assert ResponseValidator.validate_book_structure(book)
                assert isinstance(book["id"], int)
                assert isinstance(book["title"], str)
                assert isinstance(book["pageCount"], int)

    def test_get_all_books_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting all books is reasonable.
        """
        # Act & Assert
        response = books_api_client.get_all_books()

        # Response should be under 5 seconds for good performance
        assert response.elapsed.total_seconds() < 5.0
        assert response.status_code == 200

    def test_get_all_books_headers(self, books_api_client: BooksClient) -> None:
        """
        Test response headers for getting all books.
        """
        # Act
        response = books_api_client.get_all_books()

        # Assert
        assert response.status_code == 200
        assert "content-type" in response.headers

        # API should return JSON content type
        assert "application/json" in response.headers.get("content-type", "").lower()


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
        assert ResponseValidator.validate_status_code(response, 200)
        assert ResponseValidator.validate_content_type(response)
        assert ResponseValidator.validate_json_response(response)

        book_data = response.json()
        assert ResponseValidator.validate_book_structure(book_data)
        assert book_data["id"] == book_id
        assert isinstance(book_data["title"], str)
        assert len(book_data["title"]) > 0

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

        assert ResponseValidator.validate_error_response(response)

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

        # Assert - Should return 400 Bad Request or 404
        assert response.status_code in [400, 404]
        assert ResponseValidator.validate_error_response(response)

    def test_get_book_response_time(self, books_api_client: BooksClient) -> None:
        """
        Test response time for getting single book.
        """
        # Act
        response = books_api_client.get_book_by_id(1)

        # Assert
        assert response.elapsed.total_seconds() < 3.0
        assert response.status_code == 200
