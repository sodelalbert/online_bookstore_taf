"""
Tests for Authors API - PUT endpoints.
"""

import pytest
from jsonschema import validate
from src.clients.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels


@pytest.mark.api
class TestPutAuthors:
    """
    Test suite for PUT /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_put_author_success(self, authors_api_client: AuthorsClient) -> None:
        """
        Test successful update of author.

        Sunny day scenario: API returns 200 status with updated author data.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        post_author_response = post_response.json()

        author_id = post_author_response["id"]

        updated_author_data = AuthorsData.updated_author_data

        # Act
        update_response = authors_api_client.update_author(
            author_id, updated_author_data
        )

        # Assert
        assert update_response.status_code == 200
        assert "application/json" in update_response.headers.get("content-type", "")
        updated_author_response = update_response.json()

        validate(updated_author_response, AuthorModels.author_response_model)

        assert updated_author_response["id"] == author_id
        assert updated_author_response["idBook"] == updated_author_data["idBook"]
        assert updated_author_response["firstName"] == updated_author_data["firstName"]
        assert updated_author_response["lastName"] == updated_author_data["lastName"]

    def test_put_author_nonexistent_id(self, authors_api_client: AuthorsClient) -> None:
        """
        Test update of author with non-existent ID.

        Edge case: API should return 404 Not Found for non-existent author.
        """

        # Arrange
        nonexistent_author_id = 999999
        updated_author_data = AuthorsData.updated_author_data

        # Act
        update_response = authors_api_client.update_author(
            nonexistent_author_id, updated_author_data
        )

        # Assert
        assert update_response.status_code == 404

    def test_put_author_invalid_data(self, authors_api_client: AuthorsClient) -> None:
        """
        Test update of author with invalid data.

        Edge case: API should return 400 Bad Request for invalid input.
        """

        # Arrange - First create a valid author
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        post_author_response = post_response.json()
        author_id = post_author_response["id"]

        # Arrange invalid update data
        invalid_author_data = AuthorsData.invalid_author_data

        # Act
        update_response = authors_api_client.update_author(
            author_id, invalid_author_data
        )

        # Assert
        assert update_response.status_code == 400

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
        update_response = authors_api_client.update_author(
            invalid_id, updated_author_data
        )

        # Assert
        assert update_response.status_code in [400, 404]

    def test_put_author_partial_update(self, authors_api_client: AuthorsClient) -> None:
        """
        Test partial update of author (updating only some fields).

        Edge case: Test if API supports partial updates.
        """

        # Arrange - Create initial author
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        post_author_response = post_response.json()
        author_id = post_author_response["id"]

        # Partial update data (only firstName)
        partial_update_data = {
            "idBook": test_author_data["idBook"],
            "firstName": "Partially Updated Name",
            "lastName": test_author_data["lastName"],
        }

        # Act
        update_response = authors_api_client.update_author(
            author_id, partial_update_data
        )

        # Assert
        assert update_response.status_code == 200
        updated_author_response = update_response.json()

        validate(updated_author_response, AuthorModels.author_response_model)
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
        post_author_response = post_response.json()
        author_id = post_author_response["id"]

        # Update to different book
        different_book_data = AuthorsData.sample_author_data_different_book

        # Act
        update_response = authors_api_client.update_author(
            author_id, different_book_data
        )

        # Assert
        assert update_response.status_code == 200
        updated_author_response = update_response.json()

        validate(updated_author_response, AuthorModels.author_response_model)
        assert updated_author_response["idBook"] == different_book_data["idBook"]

    def test_put_author_response_time(self, authors_api_client: AuthorsClient) -> None:
        """
        Test response time for updating author is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Arrange - Create author first
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        author_id = post_response.json()["id"]

        updated_author_data = AuthorsData.updated_author_data

        # Act
        update_response = authors_api_client.update_author(
            author_id, updated_author_data
        )

        # Assert
        assert update_response.status_code == 200
        assert update_response.elapsed.total_seconds() < 3.0
