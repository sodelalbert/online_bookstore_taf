"""
Author model for API testing.
"""

from dataclasses import dataclass


@dataclass
class AuthorModels:
    """
    JSON object representation of an author for API testing.
    """

    author_response_model = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "idBook": {"type": "integer"},
            "firstName": {"type": "string", "nullable": True},
            "lastName": {"type": "string", "nullable": True},
        },
        "required": ["id", "idBook", "firstName", "lastName"],
    }

    author_not_found_response_model = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "title": {"type": "string"},
            "status": {"type": "integer"},
            "traceId": {"type": "string"},
        },
        "required": ["type", "title", "status", "traceId"],
    }
