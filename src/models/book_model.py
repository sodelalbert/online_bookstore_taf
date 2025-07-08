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
    pageCount: int = 0
    excerpt: str = ""
    publishDate: Optional[str] = None

    def __post_init__(self) -> None:
        """
        Post-initialization validation.
        """
        if self.publishDate is None:
            self.publishDate = datetime.now().isoformat()

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

    @classmethod
    def create_sample_book(
        cls,
        title: str = "Sample Book",
        description: str = "A sample book for testing",
        page_count: int = 100,
        excerpt: str = "This is a sample excerpt",
    ) -> "BookModel":
        """Create a sample book for testing.

        Args:
            title: Book title
            description: Book description
            page_count: Number of pages
            excerpt: Book excerpt

        Returns:
            Book instance with sample data
        """
        return cls(
            title=title, description=description, pageCount=page_count, excerpt=excerpt
        )

    def is_valid(self) -> bool:
        """Check if book data is valid.

        Returns:
            True if book data is valid
        """
        return (
            bool(self.title.strip())
            and self.pageCount >= 0
            and bool(self.description.strip())
        )

    def update_fields(self, **kwargs: Any) -> None:
        """Update book fields.

        Args:
            **kwargs: Fields to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
