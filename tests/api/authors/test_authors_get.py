"""
Tests for Authors API - GET endpoints.
"""

import pytest
from jsonschema import validate
from src.clients.authors_client import AuthorsClient
from src.models.authors_models import AuthorModels
from src.utils.validators import (
    validate_content_type,
    validate_json_schema,
    validate_status_code,
)


@pytest.mark.api
class TestGetAuthors:
    """
    Test suite for GET /api/v1/Authors endpoint.
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

        for author in authors_data:
            validate_json_schema(author, AuthorModels.author_response_model)

    def test_get_all_authors_response_time(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test response time for getting all authors is reasonable.

        Edge case: Ensure API responds quickly for performance.
        """

        # Act
        response = authors_api_client.get_all_authors()

        # Assert
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 5.0


@pytest.mark.api
class TestGetAuthorById:
    """
    Test suite for GET /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.parametrize("author_id", [1, 5, 10, 50, 100])
    def test_get_author_by_valid_id_success(
        self, authors_api_client: AuthorsClient, author_id: int
    ) -> None:
        """
        Test successful retrieval of author by valid ID.

        Sunny day scenario: API returns specific author with 200 status.
        """
        # Act
        response = authors_api_client.get_author_by_id(author_id)

        # Assert
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")

        author = response.json()
        validate(author, AuthorModels.author_response_model)

    @pytest.mark.parametrize("invalid_id", [0, -1, -100, 999999, 1000000])
    def test_get_author_by_invalid_id(
        self, authors_api_client: AuthorsClient, invalid_id: int
    ) -> None:
        """
        Test retrieval of author with invalid/non-existent ID.

        Edge case: API should handle invalid IDs gracefully.
        """

        # Act
        response = authors_api_client.get_author_by_id(invalid_id)

        # Assert
        assert response.status_code == 404
        assert "application/problem+json" in response.headers.get("content-type", "")

        problem_json = response.json()
        validate(problem_json, AuthorModels.author_not_found_response_model)

    @pytest.mark.parametrize("invalid_id_type", ["abc", "12.5", "null", "undefined"])
    def test_get_author_by_invalid_id_type(
        self, authors_api_client: AuthorsClient, invalid_id_type: str
    ) -> None:
        """
        Test retrieval with invalid ID types.

        Edge case: API should handle non-integer IDs.
        """

        # Act
        response = authors_api_client.get_author_by_id(invalid_id_type)

        # Assert
        assert response.status_code == 400

        problem_json = response.json()
        validate(problem_json, AuthorModels.author_not_found_response_model)

    def test_get_author_response_time(self, authors_api_client: AuthorsClient) -> None:
        """
        Test response time for getting single author.

        Edge case: Ensure API responds quickly for performance.
        """

        # Act
        response = authors_api_client.get_author_by_id(1)

        # Assert
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 3.0
