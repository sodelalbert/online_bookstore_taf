"""
Book model for API testing.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class BookModel:
    """
    Book model representing the API book entity.
    """

    id: Optional[int] = None
    title: str = ""
    description: str = ""
    page_count: int = 0
    excerpt: str = ""
    publish_date: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Post-initialization validation.
        """
        if self.publish_date is None:
            self.publish_date = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert book to dictionary for API requests.

        Returns:
            Dictionary representation of the book
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BookModel":
        """
        Create Book instance from dictionary.

        Args:
            data: Dictionary containing book data

        Returns:
            Book instance
        """
        return cls(**data)
