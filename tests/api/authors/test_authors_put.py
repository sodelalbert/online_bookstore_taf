"""
Tests for Authors API - PUT endpoints.
"""

import pytest
from src.clients.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels
from src.utils.validators import (
    validate_content_type,
    validate_elapsed_time,
    validate_json_schema,
    validate_response_reason,
    validate_status_code,
)


@pytest.mark.api
class TestPutAuthors:
    """
    Test suite for PUT /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_put_existing_author_success(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test successful update of existing author.

        Sunny day scenario: API returns 200 status with updated author data.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)

        author_id = post_response.json()["id"]
        updated_author_data = AuthorsData.updated_author_data

        # Act
        put_response = authors_api_client.update_author(author_id, updated_author_data)

        # Assert
        validate_status_code(put_response, 200)
        validate_content_type(put_response, "application/json")
        validate_response_reason(put_response, "OK")

        updated_author_response = put_response.json()
        validate_json_schema(
            updated_author_response, AuthorModels.author_response_model
        )

        # Verify the author was actually updated
        assert updated_author_response["id"] == author_id
        assert updated_author_response["idBook"] == updated_author_data["idBook"]
        assert updated_author_response["firstName"] == updated_author_data["firstName"]
        assert updated_author_response["lastName"] == updated_author_data["lastName"]

    def test_put_nonexistent_author_failure(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test updating nonexistent author fails appropriately.

        Edge case: API should return 404 for non-existent author ID.
        """

        # Arrange
        nonexistent_author_id = 999999
        updated_author_data = AuthorsData.updated_author_data

        # Act
        put_response = authors_api_client.update_author(
            nonexistent_author_id, updated_author_data
        )

        # Assert
        validate_status_code(put_response, 404)
        validate_response_reason(put_response, "Not Found")

        put_response_json = put_response.json()
        validate_json_schema(
            put_response_json, AuthorModels.author_not_found_response_model
        )

    def test_put_author_with_invalid_data(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test updating author with invalid data.

        Edge case: API should handle invalid data gracefully.
        """

        # Arrange - First create a valid author
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Arrange invalid update data
        invalid_author_data = AuthorsData.invalid_author_data

        # Act
        put_response = authors_api_client.update_author(author_id, invalid_author_data)

        # Assert
        # The API behavior with invalid data may vary
        validate_status_code(put_response, [200, 400])

        if put_response.status_code == 200:
            put_response_json = put_response.json()
            validate_json_schema(put_response_json, AuthorModels.author_response_model)
        elif put_response.status_code == 400:
            validate_response_reason(put_response, "Bad Request")

    @pytest.mark.parametrize("invalid_id", [0, -1, -100, "abc", 1.5])
    def test_put_author_invalid_id_types(
        self, authors_api_client: AuthorsClient, invalid_id: int | str
    ) -> None:
        """
        Test update of author with invalid ID types.

        Edge case: API should handle invalid ID types gracefully.
        """

        # Arrange
        updated_author_data = AuthorsData.updated_author_data

        # Act
        put_response = authors_api_client.update_author(invalid_id, updated_author_data)

        # Assert
        validate_status_code(put_response, [400, 404])

    def test_put_author_partial_update(self, authors_api_client: AuthorsClient) -> None:
        """
        Test partial update of author (updating only some fields).

        Edge case: Test if API supports partial updates.
        """

        # Arrange - Create initial author
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Partial update data (only firstName)
        partial_update_data = {
            "idBook": test_author_data["idBook"],
            "firstName": "Partially Updated Name",
            "lastName": test_author_data["lastName"],
        }

        # Act
        put_response = authors_api_client.update_author(author_id, partial_update_data)

        # Assert
        validate_status_code(put_response, 200)
        updated_author_response = put_response.json()

        validate_json_schema(
            updated_author_response, AuthorModels.author_response_model
        )
        assert updated_author_response["firstName"] == "Partially Updated Name"
        assert updated_author_response["lastName"] == test_author_data["lastName"]

    def test_put_author_different_book_association(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test updating author to be associated with a different book.

        Edge case: Test changing author's book association.
        """

        # Arrange - Create initial author
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Update to different book
        different_book_data = AuthorsData.sample_author_data_different_book

        # Act
        put_response = authors_api_client.update_author(author_id, different_book_data)

        # Assert
        validate_status_code(put_response, 200)
        updated_author_response = put_response.json()

        validate_json_schema(
            updated_author_response, AuthorModels.author_response_model
        )
        assert updated_author_response["idBook"] == different_book_data["idBook"]

    def test_put_author_response_time(self, authors_api_client: AuthorsClient) -> None:
        """
        Test response time for updating author is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Arrange - Create author first
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        updated_author_data = AuthorsData.updated_author_data

        # Act
        put_response = authors_api_client.update_author(author_id, updated_author_data)

        # Assert
        validate_status_code(put_response, 200)
        validate_elapsed_time(put_response, 3.0)
