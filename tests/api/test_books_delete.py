"""
Tests for Books API - DELETE endpoints.
"""

import pytest
from jsonschema import validate
from src.api.books_client import BooksClient
from src.data.book_data import BookData
from src.models.book_models import BookModels


@pytest.mark.api
class TestDeleteBooks:
    """
    Test suite for DELETE /api/v1/Books/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_delete_book_success(self, books_api_client: BooksClient) -> None:
        """
        Test successful deletion of book.

        Sunny day scenario: API returns 200 status with deleted book data.
        """

        # Arrange
        test_book_data = BookData.sample_book_data
        post_response = books_api_client.create_book(test_book_data)
        post_book_response = post_response.json()

        book_id = post_book_response["id"]

        # Act
        delete_response = books_api_client.delete_book(book_id)

        # Assert
        assert delete_response.status_code == 200
        assert delete_response.reason == "OK"
        assert delete_response.content == b""  # Assert that there is no JSON payload

        get_book_response = books_api_client.get_book_by_id(book_id)
        assert get_book_response.status_code == 404
        assert get_book_response.reason == "Not Found"
        not_found_response = get_book_response.json()
        validate(not_found_response, BookModels.book_not_found_response_model)
