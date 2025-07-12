"""
Tests for Books API - POST endpoints.
"""

import pytest
from jsonschema import validate
from src.clients.books_client import BooksClient
from src.data.books_data import BooksData
from src.models.books_models import BookModels
from src.utils.validators import (
    validate_content_type,
    validate_json_data,
    validate_json_schema,
    validate_status_code,
)


@pytest.mark.api
class TestPostBooks:
    """
    Test suite for POST /api/v1/Books endpoint.
    """

    @pytest.mark.parametrize(
        # "book_id", [-1, 0, 1, 99, 100, 199, 200, 201, 500, 1762, 99999]
        "book_id",
        [10900],
    )
    def test_parametrized_post_book(
        self, books_api_client: BooksClient, book_id: int
    ) -> None:
        """
        Test successful creation of book with parametrized book ID.

        Sunny day scenario: API returns 200 status with created book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data.copy()
        test_book_data["id"] = book_id

        # Act
        post_response = books_api_client.create_book(test_book_data)
        validate_status_code(post_response, 200)
        validate_content_type(post_response, "application/json")
        post_response_json = post_response.json()
        validate_json_schema(post_response_json, BookModels.book_response_model)
        validate_json_data(post_response_json, test_book_data)

        # Assert

        # Validate POST response structure
        post_response_json = post_response.json()
        validate_json_schema(post_response_json, BookModels.book_response_model)
        validate_json_data(post_response_json, test_book_data)
        # validate_json_schema(post_response_json, test_book_data)

        # Validate GET response
        get_reponse = books_api_client.get_book_by_id(book_id)
        validate_status_code(get_reponse, 200)
        validate_content_type(get_reponse, "application/json")
        get_reponse_json = get_reponse.json()
        validate_json_schema(get_reponse_json, BookModels.book_response_model)
        validate_json_data(get_reponse_json, test_book_data)

    def test_post_book_nullable_data(self, books_api_client: BooksClient) -> None:
        """
        Test creation of book with nullable fields.
        Validates handling of null values with GET request.

        Sunny day scenario: API returns 200 status with created book data.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data.copy()
        test_book_data["id"] = 99999  # Use a unique ID for this test
        test_book_data["title"] = None
        test_book_data["description"] = None
        test_book_data["excerpt"] = None

        # Act
        post_response = books_api_client.create_book(test_book_data)

        # Assert

        # Validate POST response structure
        validate_status_code(post_response, 200)
        validate_content_type(post_response, "application/json")
        post_response_json = post_response.json()

        validate_json_schema(post_response_json, BookModels.book_response_model)

        # Validate created book data
        test_book_id = test_book_data.get("id")

        get_reponse = books_api_client.get_book_by_id(test_book_id)
        validate_status_code(get_reponse, 200)
        validate_content_type(get_reponse, "application/json")
        get_reponse_json = get_reponse.json()
        validate_json_schema(get_reponse_json, BookModels.book_response_model)
        validate_json_data(get_reponse_json, test_book_data)

    def test_post_conflict_book_id(self, books_api_client: BooksClient) -> None:
        """
        Test creation of book with existing ID.

        Edge case: API should return 400 or 409 Conflict for duplicate ID.
        """

        # Arrange
        get_response = books_api_client.get_book_by_id(1)

        validate_status_code(get_response, 200)

        existing_book_data = get_response.json()
        assert existing_book_data["id"] == 1
        assert existing_book_data["pageCount"] is not None
        assert existing_book_data["publishDate"] is not None

        test_book_data = BooksData.sample_book_data
        test_book_data["id"] = 1

        # Act
        post_response = books_api_client.create_book(test_book_data)

        # Assert
        validate_status_code(post_response, [400, 409])
        validate_content_type(post_response, "application/json")

    def test_post_book_missing_mandatory_data(
        self, books_api_client: BooksClient
    ) -> None:
        """
        Test creation of book with missing data.

        Edge case: API should return 400 Bad Request for invalid input.
        """

        # Arrange
        invalid_book_data = BooksData.invalid_book_data.copy()

        # Act
        post_response = books_api_client.create_book(invalid_book_data)

        # Assert
        validate_status_code(post_response, 400)
        validate_content_type(post_response, "application/problem+json")

        post_reponse_json = post_response.json()
        validate(post_reponse_json, BookModels.book_not_found_response_model)

    def test_post_out_of_range_page_count(self, books_api_client: BooksClient) -> None:
        """
        Test creation of book with out-of-range page count.

        Edge case: API should return 400 Bad Request for invalid ID.
        """

        # Arrange
        test_book_data = BooksData.sample_book_data
        test_book_data["pageCount"] = -1020

        # Act
        post_response = books_api_client.create_book(test_book_data)

        # Assert
        validate_status_code(post_response, 400)
        validate_content_type(post_response, "application/problem+json")
        post_reponse_json = post_response.json()
        validate(post_reponse_json, BookModels.book_not_found_response_model)
