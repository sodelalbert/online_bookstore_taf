"""
Tests for Authors API - DELETE endpoints.
"""

import pytest
from jsonschema import validate
from src.api.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels


@pytest.mark.api
class TestDeleteAuthors:
    """
    Test suite for DELETE /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_delete_author_success(self, authors_api_client: AuthorsClient) -> None:
        """
        Test successful deletion of author.

        Sunny day scenario: API returns 200 status with deleted author data.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        post_author_response = post_response.json()

        author_id = post_author_response["id"]

        # Act
        delete_response = authors_api_client.delete_author(author_id)

        # Assert
        assert delete_response.status_code == 200
        assert delete_response.reason == "OK"
        assert delete_response.content == b""  # Assert that there is no JSON payload

        # Verify author is actually deleted by trying to get it
        get_author_response = authors_api_client.get_author_by_id(author_id)
        assert get_author_response.status_code == 404
        assert get_author_response.reason == "Not Found"
        not_found_response = get_author_response.json()
        validate(not_found_response, AuthorModels.author_not_found_response_model)

    def test_delete_author_nonexistent_id(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test deletion of author with non-existent ID.

        Edge case: API should return 404 Not Found for non-existent author.
        """

        # Arrange
        nonexistent_author_id = 999999

        # Act
        delete_response = authors_api_client.delete_author(nonexistent_author_id)

        # Assert
        assert delete_response.status_code == 404

    @pytest.mark.parametrize("invalid_id", [0, -1, -100])
    def test_delete_author_invalid_negative_ids(
        self, authors_api_client: AuthorsClient, invalid_id: int
    ) -> None:
        """
        Test deletion of author with invalid negative IDs.

        Edge case: API should handle invalid IDs gracefully.
        """

        # Act
        delete_response = authors_api_client.delete_author(invalid_id)

        # Assert
        assert delete_response.status_code in [400, 404]

    @pytest.mark.parametrize("invalid_id_type", ["abc", "12.5", "null", "undefined"])
    def test_delete_author_invalid_id_types(
        self, authors_api_client: AuthorsClient, invalid_id_type: str
    ) -> None:
        """
        Test deletion with invalid ID types.

        Edge case: API should handle non-integer IDs gracefully.
        """

        # Act
        # Note: We need to call the delete endpoint directly with string ID
        # since our client method expects int
        response = authors_api_client.delete(f"/api/v1/Authors/{invalid_id_type}")

        # Assert
        assert response.status_code in [400, 404]

    def test_delete_author_twice(self, authors_api_client: AuthorsClient) -> None:
        """
        Test deleting the same author twice.

        Edge case: Second deletion should return 404.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        author_id = post_response.json()["id"]

        # Act - Delete once
        first_delete_response = authors_api_client.delete_author(author_id)
        assert first_delete_response.status_code == 200

        # Act - Delete again
        second_delete_response = authors_api_client.delete_author(author_id)

        # Assert
        assert second_delete_response.status_code == 404

    def test_delete_multiple_authors_in_sequence(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test deleting multiple authors in sequence.

        Edge case: Ensure multiple deletions work independently.
        """

        # Arrange - Create multiple authors
        authors_to_delete = []
        for i in range(3):
            author_data = {
                "idBook": 1,
                "firstName": f"Test Author {i}",
                "lastName": f"Test Last Name {i}",
            }
            post_response = authors_api_client.create_author(author_data)
            authors_to_delete.append(post_response.json()["id"])

        # Act & Assert - Delete each author
        for author_id in authors_to_delete:
            delete_response = authors_api_client.delete_author(author_id)
            assert delete_response.status_code == 200

            # Verify each is deleted
            get_response = authors_api_client.get_author_by_id(author_id)
            assert get_response.status_code == 404

    def test_delete_author_and_verify_other_authors_unaffected(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test that deleting one author doesn't affect other authors.

        Edge case: Ensure deletion is isolated.
        """

        # Arrange - Create two authors
        author1_data = AuthorsData.sample_author_data
        author2_data = AuthorsData.sample_author_data_different_book

        post_response1 = authors_api_client.create_author(author1_data)
        post_response2 = authors_api_client.create_author(author2_data)

        author1_id = post_response1.json()["id"]
        author2_id = post_response2.json()["id"]

        # Act - Delete only first author
        delete_response = authors_api_client.delete_author(author1_id)
        assert delete_response.status_code == 200

        # Assert - First author is deleted, second is still accessible
        get_author1_response = authors_api_client.get_author_by_id(author1_id)
        assert get_author1_response.status_code == 404

        get_author2_response = authors_api_client.get_author_by_id(author2_id)
        assert get_author2_response.status_code == 200
        validate(get_author2_response.json(), AuthorModels.author_response_model)

    def test_delete_author_response_time(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test response time for deleting author is reasonable.

        Performance test: Ensure API responds quickly.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        author_id = post_response.json()["id"]

        # Act
        delete_response = authors_api_client.delete_author(author_id)

        # Assert
        assert delete_response.status_code == 200
        assert delete_response.elapsed.total_seconds() < 3.0
