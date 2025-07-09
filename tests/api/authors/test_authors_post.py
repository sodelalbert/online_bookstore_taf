"""
Tests for Authors API - POST endpoints.
"""

import pytest
from jsonschema import validate
from src.api.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels


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
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        post_author_response = response.json()

        validate(post_author_response, AuthorModels.author_response_model)

        assert isinstance(post_author_response["id"], int)
        assert post_author_response["idBook"] == test_author_data["idBook"]
        assert post_author_response["firstName"] == test_author_data["firstName"]
        assert post_author_response["lastName"] == test_author_data["lastName"]

    def test_post_author_invalid_data(self, authors_api_client: AuthorsClient) -> None:
        """
        Test creation of author with invalid data.

        Edge case: API should return 400 Bad Request for invalid input.
        """

        # Arrange
        invalid_author_data = AuthorsData.invalid_author_data

        # Act
        response = authors_api_client.create_author(invalid_author_data)

        # Assert
        assert response.status_code == 400
        assert "application/json" in response.headers.get("content-type", "")
        error_response = response.json()

        validate(error_response, AuthorModels.author_not_found_response_model)

    def test_post_author_missing_required_fields(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test creation of author with missing required fields.

        Edge case: API should return 400 Bad Request for missing fields.
        """

        # Arrange
        incomplete_author_data = {
            "firstName": "Test Author"
            # Missing idBook and lastName
        }

        # Act
        response = authors_api_client.create_author(incomplete_author_data)

        # Assert
        assert response.status_code == 400

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
        assert response.status_code == 200
        post_author_response = response.json()

        # Verify extra fields are not in response
        assert "extraField" not in post_author_response
        assert "anotherExtraField" not in post_author_response

        # Verify valid fields are present
        validate(post_author_response, AuthorModels.author_response_model)

    @pytest.mark.parametrize("book_id", [1, 2, 5, 10, 50])
    def test_post_author_with_different_book_ids(
        self, authors_api_client: AuthorsClient, book_id: int
    ) -> None:
        """
        Test creation of authors for different book IDs.

        Edge case: Ensure authors can be created for various book IDs.
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
        assert response.status_code == 200
        post_author_response = response.json()

        validate(post_author_response, AuthorModels.author_response_model)
        assert post_author_response["idBook"] == book_id

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
        assert response.status_code == 200
        assert response.elapsed.total_seconds() < 3.0
