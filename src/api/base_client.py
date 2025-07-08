"""
HTTP client base abstract class for API testing.
"""

from abc import ABC
import os
import requests
from typing import Dict, Any, Optional
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
                "Base URL must be set in environment variables (.env) file."
            )

        self.timeout = timeout
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self) -> None:
        """
        Configure the HTTP session.
        """
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

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

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=self.timeout,
            )

            return response

        except requests.exceptions.RequestException as e:
            raise

    def get(
        self, endpoint: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        """
        GET request.
        """
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        POST request.
        """
        return self._make_request("POST", endpoint, data=data)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        PUT request.
        """
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> requests.Response:
        """
        DELETE request.
        """
        return self._make_request("DELETE", endpoint)

    def patch(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        PATCH request.
        """
        return self._make_request("PATCH", endpoint, data=data)
