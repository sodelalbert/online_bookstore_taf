"""
Global pytest configuration and fixtures.
"""

from typing import Generator
from pathlib import Path
from datetime import datetime
import logging
import pytest
from src.clients.books_client import BooksClient
from src.clients.authors_client import AuthorsClient


LOG_DIR = Path("reports/logs")
LOG_DIR.mkdir(exist_ok=True)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_call(item: pytest.Function) -> Generator[None, None, None]:
    """
    Log test start and end messages.
    """
    logger = logging.getLogger()
    logger.info(">>>>>> Test Start: %s <<<<<<", item.nodeid)
    yield
    logger.info(">>>>>> Test End: %s <<<<<<\n\n\n", item.nodeid)


@pytest.fixture(scope="session", autouse=True)
def logging_session() -> Generator[None, None, None]:
    """
    Setup and teardown logging for the entire test session.
    All test logs are combined into a single file.
    """
    session_date = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"{session_date}_test_session.log"

    logger = logging.getLogger()
    logger.handlers.clear()  # Clear existing handlers

    file_handler = logging.FileHandler(log_file, mode="a")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    yield

    logger.handlers.clear()


@pytest.fixture(scope="session")
def books_api_client() -> Generator[BooksClient, None, None]:
    """
    Create Books API client for testing.

    Yields:
        BooksAPIClient instance
    """
    client = BooksClient()
    yield client


@pytest.fixture(scope="session")
def authors_api_client() -> Generator[AuthorsClient, None, None]:
    """
    Create Authors API client for testing.

    Yields:
        AuthorsClient instance
    """
    client = AuthorsClient()
    yield client
