"""
HTTP client base abstract class for API testing.
"""

from abc import ABC
import logging
from typing import Dict, Any, Optional
import os
import requests
from dotenv import load_dotenv


class BaseClient(ABC):
    """
    HTTP Base Client wrapper for API testing.
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize API client and load configuration files.

        Args:
            base_url: Base URL for the API
            timeout: Request timeout in seconds
        """

        load_dotenv()

        self.base_url = os.getenv("BOOKS_API_BASE_URL")

        if not self.base_url:
            raise ValueError(
                "Base URL must be set in environment variables (.env) file in project root."
            )

        self.timeout = timeout
        logging.info("Base URL: %s", self.base_url)
        logging.info("HTTP Response Timeout: %s seconds", self.timeout)

        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """
        Configure the HTTP session.
        """
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    # pylint: disable=too-many-arguments,too-many-positional-arguments
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> requests.Response:
        """
        Make HTTP request with logging and error handling.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers

        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Merge headers
        request_headers = dict(self.session.headers).copy()

        if headers:
            request_headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=request_headers,
            timeout=self.timeout,
        )

        return response

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        """
        GET request.
        """
        logging.info("[GET REQ] Endpoint: %s, Params: %s", endpoint, params)
        response = self._make_request("GET", endpoint, params=params)
        logging.info(
            "[GET RSP] Code: %s, Data: %s", response.status_code, response.text
        )
        return response

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        POST request.
        """
        logging.info("[POST REQ] Endpoint: %s, Data: %s", endpoint, data)
        response = self._make_request("POST", endpoint, data=data)
        logging.info(
            "[POST RSP] Code: %s, Data: %s", response.status_code, response.text
        )
        return response

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        PUT request.
        """
        logging.info("[PUT REQ] Endpoint: %s, Data: %s", endpoint, data)
        response = self._make_request("PUT", endpoint, data=data)
        logging.info(
            "[PUT RSP] Code: %s, Data: %s", response.status_code, response.text
        )
        return response

    def delete(self, endpoint: str) -> requests.Response:
        """
        DELETE request.
        """
        logging.info("[DELETE REQ] Endpoint: %s", endpoint)
        response = self._make_request("DELETE", endpoint)
        logging.info(
            "[DELETE RSP] Code: %s, Data: %s", response.status_code, response.text
        )
        return response

    def patch(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        PATCH request.
        """
        logging.info("[PATCH REQ] Endpoint: %s, Data: %s", endpoint, data)
        response = self._make_request("PATCH", endpoint, data=data)
        logging.info(
            "[PATCH RSP] Code: %s, Data: %s", response.status_code, response.text
        )
        return response
