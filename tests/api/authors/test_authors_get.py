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
    validate_response_reason,
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
        get_response = authors_api_client.get_all_authors()

        # Assert
        validate_status_code(get_response, 200)
        validate_content_type(get_response, "application/json")

        authors_data = get_response.json()

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
        get_response = authors_api_client.get_all_authors()

        # Assert
        validate_status_code(get_response, 200)
        validate_elapsed_time(get_response, 3.0)


class TestGetAuthorsById:
    """
    Test suite for GET /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.parametrize("author_id", [1, 2, 500, 597, 598, 999, 1000, 10000])
    def test_get_author_by_valid_id(
        self, authors_api_client: AuthorsClient, author_id: int
    ) -> None:
        """
        Test successful retrieval of author by valid ID.

        Parametrized test: Test with various valid author IDs.
        """

        # Act
        get_response = authors_api_client.get_author_by_id(author_id)

        # Assert
        validate_status_code(get_response, 200)
        validate_content_type(get_response, "application/json")

        get_response_data = get_response.json()
        validate_json_schema(get_response_data, AuthorModels.author_response_model)

        # Verify the returned author has the requested ID
        assert get_response_data["id"] == author_id

    @pytest.mark.parametrize("invalid_id", [0, -1, 999999, "abc", 1.5])
    def test_get_author_by_invalid_id(
        self, authors_api_client: AuthorsClient, invalid_id: int | str
    ) -> None:
        """
        Test retrieval of author with invalid ID.

        Edge case: API should return 400 for invalid/non-existent author IDs.
        """

        # Act
        get_response = authors_api_client.get_author_by_id(invalid_id)

        # Assert
        validate_status_code(get_response, [400, 404])
        validate_content_type(get_response, "application/problem+json")

        error_data = get_response.json()
        validate_json_schema(error_data, AuthorModels.author_not_found_response_model)


class TestGetAuthorsByBookId:
    """
    Test suite for GET /api/v1/Authors/Book/{id} endpoint.
    """

    @pytest.mark.parametrize("book_id", [1, 2, 5, 10, 100])
    def test_get_authors_by_book_id_success(
        self, authors_api_client: AuthorsClient, book_id: int
    ) -> None:
        """
        Test successful retrieval of authors by book ID.

        Parametrized test: Test with various valid book IDs.
        """

        # Act
        get_response = authors_api_client.get_authors_by_book_id(book_id)

        # Assert
        validate_status_code(get_response, 200)
        validate_content_type(get_response, "application/json")

        authors_data = get_response.json()

        # Validate each author in the response
        for author in authors_data:
            validate_json_schema(author, AuthorModels.author_response_model)
            assert author["idBook"] == book_id

    @pytest.mark.parametrize("invalid_book_id", [0, -1])
    def test_get_authors_by_book_id_out_of_range(
        self, authors_api_client: AuthorsClient, invalid_book_id: int
    ) -> None:
        """
        Test retrieval of authors with book ID that is out of range.

        Edge case: API should handle invalid book IDs gracefully.
        """

        # Act
        get_response = authors_api_client.get_authors_by_book_id(invalid_book_id)

        # Assert
        validate_status_code(get_response, 200)
        validate_content_type(get_response, "application/json")

        get_response_data = get_response.json()
        assert isinstance(get_response_data, list)
        assert len(get_response_data) == 0  # Should return empty list for non-existent

    def test_get_authors_by_invalid_book_id(
        self,
        authors_api_client: AuthorsClient,
    ) -> None:
        """
        Test retrieval of authors with invalid book ID.

        Edge case: API should handle invalid book IDs gracefully.
        """
        invalid_book_id = "test"

        # Act
        get_response = authors_api_client.get_authors_by_book_id(invalid_book_id)

        # Assert
        validate_status_code(get_response, 400)
        validate_content_type(get_response, "application/problem+json")
        get_response_json = get_response.json()
        validate_json_schema(
            get_response_json, AuthorModels.author_not_found_response_model
        )
        validate_response_reason(get_response, "Bad Request")

    def test_get_authors_by_book_id_response_time(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test response time for getting authors by book ID is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Act
        get_response = authors_api_client.get_authors_by_book_id(1)

        # Assert
        validate_status_code(get_response, 200)
        validate_elapsed_time(get_response, 3.0)
