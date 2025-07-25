"""
Authors Data Class for API Tests
"""

from dataclasses import dataclass


@dataclass
class AuthorsData:
    """
    Data class for author data used in API tests.
    """

    sample_author_data = {
        "id": 1,
        "idBook": 1,
        "firstName": "Test Author",
        "lastName": "Test Last Name",
    }

    updated_author_data = {
        "idBook": 11,
        "firstName": "Updated Author",
        "lastName": "Updated Last Name",
    }

    invalid_author_data = {
        "idBook": -100,
        "firstName": None,
        "lastName": None,
    }

    sample_author_data_different_book = {
        "idBook": 2,
        "firstName": "Another Author",
        "lastName": "Another Last Name",
    }
