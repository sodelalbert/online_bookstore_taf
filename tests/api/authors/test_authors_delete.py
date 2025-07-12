"""
Tests for Authors API - DELETE endpoints.
"""

import pytest
from src.clients.authors_client import AuthorsClient
from src.data.authors_data import AuthorsData
from src.models.authors_models import AuthorModels
from src.utils.validators import (
    validate_elapsed_time,
    validate_json_schema,
    validate_response_reason,
    validate_status_code,
)


@pytest.mark.api
class TestDeleteAuthors:
    """
    Test suite for DELETE /api/v1/Authors/{id} endpoint.
    """

    @pytest.mark.smoke
    def test_delete_existing_author_success(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test successful deletion of existing author.

        Sunny day scenario: API returns 200 status and author is deleted.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Act
        delete_response = authors_api_client.delete_author(author_id)

        # Assert
        validate_status_code(delete_response, 200)
        validate_response_reason(delete_response, "OK")

        # Verify author is actually deleted by trying to get it
        get_author_response = authors_api_client.get_author_by_id(author_id)
        validate_status_code(get_author_response, 404)
        validate_response_reason(get_author_response, "Not Found")

        get_author_response_json = get_author_response.json()
        validate_json_schema(
            get_author_response_json, AuthorModels.author_not_found_response_model
        )

    @pytest.mark.parametrize("author_id", [-222, -1])
    def test_delete_nonexistent_author(
        self, authors_api_client: AuthorsClient, author_id: int
    ) -> None:
        """
        Test deletion of author which does not exist.

        Edge case: API should handle non-existent author IDs gracefully.
        """

        # Arrange - Verify author doesn't exist first
        get_response = authors_api_client.get_author_by_id(author_id)
        validate_status_code(get_response, 404)
        validate_response_reason(get_response, "Not Found")

        # Act
        delete_response = authors_api_client.delete_author(author_id)

        # Assert
        # API might return 200 (idempotent) or 404 (not found)
        validate_status_code(delete_response, [200, 404])

        if delete_response.status_code == 200:
            validate_response_reason(delete_response, "OK")
        elif delete_response.status_code == 404:
            validate_response_reason(delete_response, "Not Found")

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
        validate_status_code(delete_response, [200, 400, 404])

    def test_delete_author_twice(self, authors_api_client: AuthorsClient) -> None:
        """
        Test deleting the same author twice.

        Edge case: Second deletion should be idempotent or return appropriate error.
        """

        # Arrange
        test_author_data = AuthorsData.sample_author_data
        post_response = authors_api_client.create_author(test_author_data)
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Act - First deletion
        first_delete_response = authors_api_client.delete_author(author_id)
        validate_status_code(first_delete_response, 200)
        validate_response_reason(first_delete_response, "OK")

        # Act - Second deletion
        second_delete_response = authors_api_client.delete_author(author_id)

        # Assert
        # API should handle double deletion gracefully
        validate_status_code(second_delete_response, [200, 404])

        if second_delete_response.status_code == 200:
            validate_response_reason(second_delete_response, "OK")
        elif second_delete_response.status_code == 404:
            validate_response_reason(second_delete_response, "Not Found")

    def test_delete_author_and_verify_book_association(
        self, authors_api_client: AuthorsClient
    ) -> None:
        """
        Test that deleting an author doesn't affect other authors of the same book.

        Edge case: Verify book association integrity after author deletion.
        """

        # Arrange - Create two authors for the same book
        author_data_1 = AuthorsData.sample_author_data
        author_data_2 = {
            "idBook": author_data_1["idBook"],
            "firstName": "Second Author",
            "lastName": "Second Last Name",
        }

        post_response_1 = authors_api_client.create_author(author_data_1)
        post_response_2 = authors_api_client.create_author(author_data_2)

        validate_status_code(post_response_1, 200)
        validate_status_code(post_response_2, 200)

        author_id_1 = post_response_1.json()["id"]
        author_id_2 = post_response_2.json()["id"]
        book_id = author_data_1["idBook"]

        # Act - Delete first author
        delete_response = authors_api_client.delete_author(author_id_1)
        validate_status_code(delete_response, 200)

        # Assert - Second author should still exist and be associated with the book
        get_author_2_response = authors_api_client.get_author_by_id(author_id_2)
        validate_status_code(get_author_2_response, 200)

        author_2_data = get_author_2_response.json()
        assert author_2_data["idBook"] == book_id

        # Verify book still has authors (at least author 2)
        book_authors_response = authors_api_client.get_authors_by_book_id(str(book_id))
        validate_status_code(book_authors_response, 200)

        book_authors = book_authors_response.json()
        author_ids_for_book = [author["id"] for author in book_authors]

        # Author 1 should not be in the list anymore
        assert author_id_1 not in author_ids_for_book
        # Author 2 should still be in the list
        assert author_id_2 in author_ids_for_book

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
        validate_status_code(post_response, 200)
        author_id = post_response.json()["id"]

        # Act
        delete_response = authors_api_client.delete_author(author_id)

        # Assert
        validate_status_code(delete_response, 200)
        validate_elapsed_time(delete_response, 3.0)
