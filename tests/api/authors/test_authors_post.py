"""
Tests for Authors API - POST endpoints.
"""

import pytest
from src.clients.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels
from src.utils.validators import (
    validate_content_type,
    validate_elapsed_time,
    validate_json_data,
    validate_json_schema,
    validate_response_reason,
    validate_status_code,
)


@pytest.mark.api
class TestPostAuthors:
    """
    Test suite for POST /api/v1/Authors endpoint.
    """

    @pytest.mark.smoke
    def test_post_author_success(self, authors_api_client: AuthorsClient) -> None:
        """
        Test successful creation of author.

        Sunny day scenario: API returns 200 status with created author data.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data

        # Act
        response = authors_api_client.create_author(test_author_data)

        # Assert
        validate_status_code(response, 200)
        validate_content_type(response, "application/json")
        validate_response_reason(response, "OK")

        author_response = response.json()
        validate_json_schema(author_response, AuthorModels.author_response_model)

        # Verify the created author data
        validate_json_data(author_response, test_author_data)

    @pytest.mark.parametrize("author_id", [-1, 1, 2, 500, 597, 598, 999, 1000, 10000])
    def test_post_author_wihth_parametrized_id(
        self, authors_api_client: AuthorsClient, author_id: int
    ) -> None:
        """
        Test creation of author with different book IDs.

        Edge case: Ensure authors can be created for various book IDs.
        """
        # Arrange
        test_author_data = AuthorsData.sample_author_data.copy()
        test_author_data["id"] = author_id

        # Act
        post_response = authors_api_client.create_author(test_author_data)

        # Assert

        validate_status_code(post_response, 200)
        validate_content_type(post_response, "application/json")
        validate_response_reason(post_response, "OK")
        post_response = post_response.json()
        validate_json_schema(post_response, AuthorModels.author_response_model)
        validate_json_data(post_response, test_author_data)

        # Undefined behavior for author_id in response - due to ID allocaton issue.
        get_response = authors_api_client.get_author_by_id(author_id)
        validate_status_code(get_response, 200)
        validate_content_type(get_response, "application/json")
        get_response_json = get_response.json()
        validate_json_schema(get_response_json, AuthorModels.author_response_model)
        validate_json_data(get_response_json, test_author_data)

    def test_post_author_invalid_data(self, authors_api_client: AuthorsClient) -> None:
        """
        Test creation of author with invalid data.

        Edge case: API should handle invalid input appropriately.
        """

        invalid_author_data = AuthorsData.invalid_author_data

        # Act
        post_response = authors_api_client.create_author(invalid_author_data)

        # Assert
        validate_status_code(post_response, 400)
        validate_response_reason(post_response, "Bad Request")

    def test_post_author_with_extra_fields(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test creation of author with extra fields not defined in schema.

        Edge case: API should ignore extra fields and return valid author data.
        """

        # Arrange
        author_data_with_extra_fields = {
            **AuthorsData.sample_author_data,
            "extraField": "This should be ignored",
            "anotherExtraField": 12345,
        }

        # Act
        response = authors_api_client.create_author(author_data_with_extra_fields)

        # Assert
        validate_status_code(response, 200)
        author_response = response.json()

        # Verify extra fields are not in response
        assert "extraField" not in author_response
        assert "anotherExtraField" not in author_response

        # Verify valid fields are present
        validate_json_schema(author_response, AuthorModels.author_response_model)

    @pytest.mark.parametrize("book_id", [-1, 0, 1, 2, 5, 10, 50])
    def test_post_author_with_different_book_ids(
        self, authors_api_client: AuthorsClient, book_id: int
    ) -> None:
        """
        Test creation of authors for different book IDs.

        Parametrized test: Ensure authors can be created for various book IDs.
        """

        # Arrange
        author_data = {
            "idBook": book_id,
            "firstName": f"Author for Book {book_id}",
            "lastName": f"LastName {book_id}",
        }

        # Act
        response = authors_api_client.create_author(author_data)

        # Assert
        validate_status_code(response, 200)
        author_response = response.json()

        validate_json_schema(author_response, AuthorModels.author_response_model)
        assert author_response["idBook"] == book_id

    def test_post_author_response_time(self, authors_api_client: AuthorsClient) -> None:
        """
        Test response time for creating author is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data

        # Act
        response = authors_api_client.create_author(test_author_data)

        # Assert
        validate_status_code(response, 200)
        validate_elapsed_time(response, 3.0)
