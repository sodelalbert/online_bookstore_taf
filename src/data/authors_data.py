"""
Authors Data Class for API Tests
"""

from typing import Dict, Any


class AuthorsData:
    """
    Data class for book data used in API tests.
    """

    author_response_model: Dict[str, Any] = {}

    author_not_found_response_model: Dict[str, Any] = {}
