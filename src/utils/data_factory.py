"""
Test data generators and factories.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import random
import string
from src.models.book_model import BookModel


class BookDataFactory:
    """
    Factory for generating test book data.
    """

    @staticmethod
    def create_valid_book_data(**overrides: Any) -> Dict[str, Any]:
        """
        Create valid book data for testing.

        Args:
            **overrides: Override default values

        Returns:
            Dictionary with valid book data
        """
        default_data = {
            "id": random.randint(1, 1000),
            "title": f"Test Book {random.randint(1, 1000)}",
            "description": "A comprehensive test book for API validation",
            "pageCount": random.randint(50, 500),
            "excerpt": "This is a test excerpt for the book",
            "publishDate": datetime.now().isoformat(),
        }

        # Apply overrides
        default_data.update(overrides)
        return default_data

    @staticmethod
    def create_book_model(**overrides: Any) -> BookModel:
        """
        Create Book model instance with test data.

        Args:
            **overrides: Override default values

        Returns:
            Book model instance
        """
        data = BookDataFactory.create_valid_book_data(**overrides)
        # Remove ID for creation scenarios
        if "id" in data and overrides.get("remove_id", True):
            data.pop("id")
        return BookModel.from_dict(data)

    @staticmethod
    def create_invalid_book_data(invalid_field: str) -> Dict[str, Any]:
        """
        Create invalid book data for negative testing.

        Args:
            invalid_field: Field to make invalid

        Returns:
            Dictionary with invalid book data
        """
        base_data = BookDataFactory.create_valid_book_data()

        invalid_data_map = {
            "empty_title": {"title": ""},
            "null_title": {"title": None},
            "negative_pageCount": {"pageCount": -1},
            "invalid_pageCount_type": {"pageCount": "invalid"},
            "missing_description": {"description": ""},
            "null_description": {"description": None},
            "invalid_date": {"publishDate": "invalid-date"},
            "missing_excerpt": {"excerpt": ""},
            "extremely_long_title": {"title": "x" * 1000},
            "special_chars_title": {"title": "!@#$%^&*()[]{}|\\:;\"'<>?,./"},
        }

        if invalid_field in invalid_data_map:
            invalid_value = invalid_data_map[invalid_field]
            if isinstance(invalid_value, dict):
                base_data.update(invalid_value)

        return base_data

    @staticmethod
    def create_book_list(count: int = 5) -> List[Dict[str, Any]]:
        """
        Create a list of book data for testing.

        Args:
            count: Number of books to create

        Returns:
            List of book data dictionaries
        """
        books = []
        for i in range(count):
            book_data = BookDataFactory.create_valid_book_data(
                id=i + 1, title=f"Test Book {i + 1}", pageCount=random.randint(100, 400)
            )
            books.append(book_data)
        return books

    @staticmethod
    def create_random_string(length: int = 10) -> str:
        """
        Create random string for testing.

        Args:
            length: Length of random string

        Returns:
            Random string
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def create_edge_case_book_data() -> Dict[str, Dict[str, Any]]:
        """
        Create various edge case book data scenarios.

        Returns:
            Dictionary of edge case scenarios
        """
        return {
            "minimal_valid": {
                "title": "A",
                "description": "B",
                "pageCount": 1,
                "excerpt": "C",
                "publishDate": datetime.now().isoformat(),
            },
            "maximum_length_fields": {
                "title": "x" * 255,
                "description": "y" * 1000,
                "pageCount": 999999,
                "excerpt": "z" * 500,
                "publishDate": datetime.now().isoformat(),
            },
            "zero_pages": {
                "title": "Zero Page Book",
                "description": "A book with zero pages",
                "pageCount": 0,
                "excerpt": "No content",
                "publishDate": datetime.now().isoformat(),
            },
            "future_date": {
                "title": "Future Book",
                "description": "A book from the future",
                "pageCount": 200,
                "excerpt": "Future content",
                "publishDate": (datetime.now() + timedelta(days=365)).isoformat(),
            },
            "past_date": {
                "title": "Ancient Book",
                "description": "A very old book",
                "pageCount": 150,
                "excerpt": "Ancient wisdom",
                "publishDate": (datetime.now() - timedelta(days=365 * 100)).isoformat(),
            },
        }

    @staticmethod
    def create_unicode_book_data() -> Dict[str, Any]:
        """
        Create book data with various unicode characters.

        Returns:
            Dictionary with unicode book data
        """
        return BookDataFactory.create_valid_book_data(
            title="Unicode Test: 中文 العربية日本語",
            description="Special chars: àáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ",
            excerpt="Emojis and symbols: 📚📖📝✨🌟⭐💫🔖📋📌📍🎯",
        )

    @staticmethod
    def create_boundary_value_data() -> List[Dict[str, Any]]:
        """
        Create book data with boundary values.

        Returns:
            List of dictionaries with boundary value scenarios
        """
        boundary_cases = [
            # Minimum values
            BookDataFactory.create_valid_book_data(
                title="X",  # Single character
                pageCount=0,  # Minimum pages
                description="Y",  # Single character
                excerpt="Z",  # Single character
            ),
            # Maximum reasonable values
            BookDataFactory.create_valid_book_data(
                title="A" * 255,  # Long title
                pageCount=999999,  # Large page count
                description="B" * 1000,  # Long description
                excerpt="C" * 500,  # Long excerpt
            ),
            # Negative edge cases (should be invalid)
            {
                "title": "Negative Pages Test",
                "description": "Testing negative page count",
                "pageCount": -1,
                "excerpt": "Should be invalid",
                "publishDate": datetime.now().isoformat(),
            },
        ]
        return boundary_cases

    @staticmethod
    def create_malformed_data_sets() -> Dict[str, Dict[str, Any]]:
        """
        Create various malformed data sets for negative testing.

        Returns:
            Dictionary of malformed data scenarios
        """
        return {
            "missing_required_fields": {
                "title": "Incomplete Book"
                # Missing other required fields
            },
            "wrong_data_types": {
                "title": 12345,  # Should be string
                "description": ["not", "a", "string"],  # Should be string
                "pageCount": "not_a_number",  # Should be int
                "excerpt": {"not": "a_string"},  # Should be string
                "publishDate": 20240101,  # Should be string
            },
            "null_values": {
                "title": None,
                "description": None,
                "pageCount": None,
                "excerpt": None,
                "publishDate": None,
            },
            "empty_strings": {
                "title": "",
                "description": "",
                "pageCount": 100,  # Keep valid
                "excerpt": "",
                "publishDate": datetime.now().isoformat(),  # Keep valid
            },
            "extremely_long_values": {
                "title": "X" * 10000,  # Extremely long
                "description": "Y" * 50000,  # Extremely long
                "pageCount": 999999999,  # Extremely large number
                "excerpt": "Z" * 10000,  # Extremely long
                "publishDate": datetime.now().isoformat(),
            },
        }

    @staticmethod
    def create_update_scenarios() -> Dict[str, Dict[str, Any]]:
        """
        Create various update scenarios for PUT testing.

        Returns:
            Dictionary of update scenarios
        """
        base_id = random.randint(1, 1000)
        return {
            "complete_update": BookDataFactory.create_valid_book_data(
                id=base_id,
                title="Completely Updated Book",
                description="Every field has been updated",
                pageCount=999,
                excerpt="New excerpt content",
                publishDate="2024-12-31T23:59:59",
            ),
            "partial_update_title_only": {"id": base_id, "title": "Only Title Updated"},
            "partial_update_content": {
                "id": base_id,
                "title": "Updated Title",
                "description": "Updated Description",
                "pageCount": 555,
            },
            "unicode_update": {
                "id": base_id,
                "title": "Unicode Update: 测试更新",
                "description": "تحديث باللغة العربية",
                "excerpt": "Обновление на русском языке",
            },
            "special_chars_update": {
                "id": base_id,
                "title": "Special !@#$%^&*() Update",
                "description": "Testing <script>alert('xss')</script> injection",
                "excerpt": "SQL'; DROP TABLE books; --",
            },
        }
