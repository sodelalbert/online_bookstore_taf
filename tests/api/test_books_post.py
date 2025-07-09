# """
# Tests for Books API - POST endpoint.
# """

# import pytest
# from typing import Dict, Any
# from src.api.books_client import BooksClient
# from src.utils.validators import ResponseValidator
# from src.utils.data_factory import BookDataFactory
# from src.models.book_model import BookModel


# @pytest.mark.api
# class TestCreateBook:
#     """
#     Test suite for POST /api/v1/Books endpoint.
#     """

#     @pytest.mark.smoke
#     def test_create_book_success(
#         self,
#         books_api_client: BooksClient,
#         sample_book_data: Dict[str, Any],
#     ) -> None:
#         """
#         Test successful book creation.

#         Sunny day scenario: Create book with valid data.
#         """
#         # Act
#         response = books_api_client.create_book(sample_book_data)

#         # Assert
#         assert response.status_code == 200
#         assert ResponseValidator.validate_content_type(response)
#         assert ResponseValidator.validate_json_response_format(response)

#         created_book = response.json()
#         assert ResponseValidator.validate_book_structure(created_book)

#         # Verify created book data matches input
#         assert created_book["title"] == sample_book_data["title"]
#         assert created_book["description"] == sample_book_data["description"]
#         assert created_book["pageCount"] == sample_book_data["pageCount"]
#         assert created_book["excerpt"] == sample_book_data["excerpt"]

#         # Verify ID was assigned
#         assert "id" in created_book
#         assert isinstance(created_book["id"], int)
#         assert created_book["id"] > 0

#     # def test_create_book_with_model(
#     #     self,
#     #     books_api_client: BooksClient,
#     # ) -> None:
#     #     """
#     #     Test creating book using Book model.
#     #     """
#     #     # Arrange
#     #     book_model = BookDataFactory.create_book_model(
#     #         title="Model Test Book",
#     #         description="Book created using model",
#     #         pageCount=150,
#     #     )

#     #     # Act
#     #     response = books_api_client.create_book_from_model(book_model)

#     #     # Assert
#     #     assert response.status_code == 200
#     #     assert ResponseValidator.validate_json_response(response)

#     #     created_book = response.json()
#     #     assert created_book["title"] == "Model Test Book"
#     #     assert created_book["description"] == "Book created using model"
#     #     assert created_book["pageCount"] == 150

#     def test_create_book_with_unicode_characters(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with unicode and special characters.
#         """
#         # Arrange
#         unicode_data = BookDataFactory.create_unicode_book_data()

#         # Act
#         response = books_api_client.create_book(unicode_data)

#         # Assert
#         assert response.status_code == 200
#         created_book = response.json()

#         # Verify unicode characters are preserved
#         assert "中文" in created_book["title"]
#         assert "العربية" in created_book["title"]
#         assert "📚" in created_book["excerpt"]

#     def test_create_book_boundary_values(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with boundary values.
#         """
#         boundary_cases = BookDataFactory.create_boundary_value_data()

#         # Test minimum values
#         min_values_data = boundary_cases[0]
#         response = books_api_client.create_book(min_values_data)

#         assert response.status_code == 200
#         created_book = response.json()
#         assert len(created_book["title"]) >= 1
#         assert created_book["pageCount"] >= 0

#     def test_create_book_with_empty_data(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with completely empty data.
#         """
#         empty_data = {}
#         response = books_api_client.create_book(empty_data)
#         assert response.status_code in [400, 422]

#     def test_create_book_with_missing_title(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with missing required 'title' field.
#         """
#         missing_title = {
#             "description": "Book without title",
#             "pageCount": 100,
#             "excerpt": "No title excerpt",
#             "publishDate": "2024-01-01T00:00:00.000Z",
#         }
#         response = books_api_client.create_book(missing_title)
#         assert response.status_code in [200, 400, 422]

#     def test_create_book_with_negative_page_count(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with negative page count.
#         """
#         # Arrange
#         negative_data = BookDataFactory.create_boundary_value_data()[2]  # Negative case

#         # Act
#         response = books_api_client.create_book(negative_data)

#         # Assert - Should reject negative page count
#         assert response.status_code in [400, 422]

#     def test_create_book_with_null_values(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with null values.
#         """
#         # Arrange
#         null_data = BookDataFactory.create_malformed_data_sets()["null_values"]

#         # Act
#         response = books_api_client.create_book(null_data)

#         # Assert
#         assert response.status_code in [400, 422]

#     def test_create_duplicate_books(
#         self,
#         books_api_client: BooksClient,
#         sample_book_data: Dict[str, Any],
#     ) -> None:
#         """
#         Test creating multiple books with identical data.
#         """
#         # Create first book
#         response1 = books_api_client.create_book(sample_book_data)
#         assert response1.status_code == 200
#         book1 = response1.json()

#         # Create second book with identical data
#         response2 = books_api_client.create_book(sample_book_data)
#         assert response2.status_code == 200
#         book2 = response2.json()

#         # Should create separate books with different IDs
#         assert book1["id"] != book2["id"]
#         assert book1["title"] == book2["title"]

#     def test_create_book_with_special_injection_attempts(
#         self,
#         books_api_client: BooksClient,
#     ) -> None:
#         """
#         Test creating book with potential injection attacks.
#         """
#         injection_data = {
#             "title": "<script>alert('XSS')</script>",
#             "description": "SQL'; DROP TABLE books; --",
#             "pageCount": 100,
#             "excerpt": "Testing injection",
#             "publishDate": "2024-01-01T00:00:00.000Z",
#         }

#         # Act
#         response = books_api_client.create_book(injection_data)

#         # Assert - Should handle injection attempts safely
#         assert response.status_code in [200, 400, 422]

#         if response.status_code == 200:
#             # If accepted, verify dangerous content is sanitized
#             created_book = response.json()
#             # Should not contain raw script tags or SQL commands
#             assert "<script>" not in created_book.get("title", "")
#             assert "DROP TABLE" not in created_book.get("description", "")

#     def test_create_book_response_time(
#         self,
#         books_api_client: BooksClient,
#         sample_book_data: Dict[str, Any],
#     ) -> None:
#         """
#         Test response time for book creation.
#         """
#         # Act
#         response = books_api_client.create_book(sample_book_data)

#         # Assert
#         assert response.elapsed.total_seconds() < 5.0
#         assert response.status_code == 200
