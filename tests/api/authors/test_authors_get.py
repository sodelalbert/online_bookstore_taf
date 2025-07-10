"""
Tests for Authors API - GET endpoints.
"""

import pytest
from src.clients.authors_client import AuthorsClient
from src.models.authors_models import AuthorModels
from src.utils.validators import (
    validate_content_type,
    validate_elapsed_time,
    validate_json_schema,
    validate_status_code,
)


@pytest.mark.api
class TestGetAuthors:
    """
    Test suite for GET /api/v1/Authors endpoints.
    """

    @pytest.mark.smoke
    def test_get_all_authors_success(self, authors_api_client: AuthorsClient) -> None:
        """
        Test successful retrieval of all authors.

        Sunny day scenario: API returns list of authors with 200 status.
        """

        # Act
        response = authors_api_client.get_all_authors()

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")

        authors_data = response.json()

        # Validate each author in the response
        for author in authors_data:
            validate_json_schema(author, AuthorModels.author_response_model)

    def test_get_all_authors_response_time(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test response time for getting all authors is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Act
        response = authors_api_client.get_all_authors()

        # Assert
        validate_status_code(response, 200)
        validate_elapsed_time(response, 3.0)

    @pytest.mark.parametrize("author_id", [1, 2, 5, 10, 50])
    def test_get_author_by_valid_id(
        self, authors_api_client: AuthorsClient, author_id: int
    ) -> None:
        """
        Test successful retrieval of author by valid ID.

        Parametrized test: Test with various valid author IDs.
        """

        # Act
        response = authors_api_client.get_author_by_id(author_id)

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")

        author_data = response.json()
        validate_json_schema(author_data, AuthorModels.author_response_model)

        # Verify the returned author has the requested ID
        assert author_data["id"] == author_id

    @pytest.mark.parametrize("invalid_id", [0, -1, 999999, "abc", 1.5])
    def test_get_author_by_invalid_id(
        self, authors_api_client: AuthorsClient, invalid_id
    ) -> None:
        """
        Test retrieval of author with invalid ID.

        Edge case: API should return 400 for invalid/non-existent author IDs.
        """

        # Act
        response = authors_api_client.get_author_by_id(invalid_id)

        # Assert
        validate_status_code(response, [400, 404])
        validate_content_type(response, "application/problem+json")

        error_data = response.json()
        validate_json_schema(error_data, AuthorModels.author_not_found_response_model)

    @pytest.mark.parametrize("book_id", [1, 2, 5, 10])
    def test_get_authors_by_book_id_success(
        self, authors_api_client: AuthorsClient, book_id: int
    ) -> None:
        """
        Test successful retrieval of authors by book ID.

        Parametrized test: Test with various valid book IDs.
        """

        # Act
        response = authors_api_client.get_authors_by_book_id(book_id)

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")

        authors_data = response.json()

        # Validate each author in the response
        for author in authors_data:
            validate_json_schema(author, AuthorModels.author_response_model)
            # Verify all authors belong to the requested book
            assert author["idBook"] == book_id

    @pytest.mark.parametrize("invalid_book_id", [0, -1, 999999])
    def test_get_authors_by_invalid_book_id(
        self, authors_api_client: AuthorsClient, invalid_book_id: int
    ) -> None:
        """
        Test retrieval of authors with invalid book ID.

        Edge case: API should handle invalid book IDs gracefully.
        """

        # Act
        response = authors_api_client.get_authors_by_book_id(invalid_book_id)

        # Assert
        # The API might return 200 with empty list or 404
        validate_status_code(response, [200, 404])

        if response.status_code == 200:
            authors_data = response.json()
            # Should return empty list for non-existent book
            assert isinstance(authors_data, list)
        elif response.status_code == 404:
            validate_content_type(response, "application/json")

    def test_get_authors_by_book_id_response_time(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test response time for getting authors by book ID is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Act
        response = authors_api_client.get_authors_by_book_id(1)

        # Assert
        validate_status_code(response, 200)
        validate_elapsed_time(response, 3.0)
