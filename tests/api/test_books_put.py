"""
Tests for Books API - PUT endpoints.
"""

import pytest
from jsonschema import validate
from src.api.books_client import BooksClient
from src.data.book_data import BookData
from src.models.book_models import BookModels


@pytest.mark.api
class TestPutBooks:
    """
    Test suite for PUT /api/v1/Books/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_put_book_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful update of book.

        Sunny day scenario: API returns 200 status with updated book data.
        """

        # Arrange
        test_book_data = BookData.sample_book_data
        post_response = books_api_client.create_book(test_book_data)
        post_book_response = post_response.json()

        book_id = post_book_response["id"]

        updated_book_data = BookData.updated_book_data

        # Act

        update_response = books_api_client.update_book(book_id, updated_book_data)

        # Assert

        assert update_response.status_code == 200
        assert "application/json" in update_response.headers.get("content-type", "")
        updated_book_response = update_response.json()

        validate(updated_book_response, BookModels.book_response_model)

        assert updated_book_response["id"] == book_id
        assert updated_book_response["title"] == updated_book_data["title"]
        assert updated_book_response["description"] == updated_book_data["description"]
        assert updated_book_response["pageCount"] == updated_book_data["pageCount"]
        assert updated_book_response["excerpt"] == updated_book_data["excerpt"]
        assert updated_book_response["publishDate"] == updated_book_data["publishDate"]
