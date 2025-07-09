"""
Book model for API testing.
"""

from dataclasses import dataclass


@dataclass
class BookModels:
    """
    JSON object representation of a book for API testing.
    """

    book_response_model = {
        "type": "object",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string", "nullable": True},
                "description": {"type": "string", "nullable": True},
                "pageCount": {"type": "integer"},
                "excerpt": {"type": "string", "nullable": True},
                "publishDate": {"type": "string", "format": "date-time"},
            },
            "required": ["id", "pageCount", "publishDate"],
        },
    }

    book_not_found_response_model = {
        "type": "object",
        "properties": {
            "type": {"type": "string"},
            "title": {"type": "string"},
            "status": {"type": "integer"},
            "traceId": {"type": "string"},
        },
        "required": ["type", "title", "status", "traceId"],
    }
