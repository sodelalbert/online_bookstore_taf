"""
Response validation utilities.
"""

import json
from typing import Any, Dict, List, Optional, Union
from requests import Response


class ResponseValidator:
    """
    Utility class for validating API responses.
    """

    @staticmethod
    def validate_status_code(response: Response, expected_code: int) -> bool:
        """
        Validate response status code.

        Args:
            response: HTTP response object
            expected_code: Expected status code

        Returns:
            True if status code matches expected
        """
        return response.status_code == expected_code

    @staticmethod
    def validate_content_type(
        response: Response, expected_type: str = "application/json"
    ) -> bool:
        """
        Validate response content type.

        Args:
            response: HTTP response object
            expected_type: Expected content type

        Returns:
            True if content type matches expected
        """
        content_type = response.headers.get("content-type", "")
        return expected_type in content_type.lower()

    @staticmethod
    def validate_json_response(response: Response) -> bool:
        """
        Validate that response contains valid JSON.

        Args:
            response: HTTP response object

        Returns:
            True if response contains valid JSON
        """
        try:
            response.json()
            return True
        except (json.JSONDecodeError, ValueError):
            return False

    @staticmethod
    def validate_required_fields(
        data: Dict[str, Any], required_fields: List[str]
    ) -> bool:
        """
        Validate that required fields are present in data.

        Args:
            data: Data dictionary to validate
            required_fields: List of required field names

        Returns:
            True if all required fields are present
        """
        return all(field in data for field in required_fields)

    @staticmethod
    def validate_field_types(
        data: Dict[str, Any], field_types: Dict[str, type]
    ) -> bool:
        """
        Validate field types in data.

        Args:
            data: Data dictionary to validate
            field_types: Dictionary mapping field names to expected types

        Returns:
            True if all fields have correct types
        """
        for field, expected_type in field_types.items():
            if field in data:
                if not isinstance(data[field], expected_type):
                    return False
        return True

    @staticmethod
    def validate_book_structure(book_data: Dict[str, Any]) -> bool:
        """
        Validate book data structure.

        Args:
            book_data: Book data to validate

        Returns:
            True if book structure is valid
        """
        required_fields = [
            "id",
            "title",
            "description",
            "pageCount",
            "excerpt",
            "publishDate",
        ]
        field_types = {
            "id": int,
            "title": str,
            "description": str,
            "pageCount": int,
            "excerpt": str,
            "publishDate": str,
        }

        return ResponseValidator.validate_required_fields(
            book_data, required_fields
        ) and ResponseValidator.validate_field_types(book_data, field_types)

    @staticmethod
    def validate_error_response(response: Response) -> bool:
        """
        Validate error response structure.

        Args:
            response: HTTP response object

        Returns:
            True if error response is valid
        """
        if response.status_code >= 400:
            return True
        return False

    @staticmethod
    def validate_delete_response(response: Response) -> bool:
        """
        Validate DELETE response structure.

        Args:
            response: HTTP response object

        Returns:
            True if delete response is valid
        """
        if response.status_code in [200, 204]:
            return True
        elif response.status_code == 404:
            return True
        return False

    @staticmethod
    def validate_update_response(
        response: Response, expected_book_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Validate PUT/UPDATE response structure.

        Args:
            response: HTTP response object
            expected_book_data: Expected book data after update

        Returns:
            True if update response is valid
        """
        if response.status_code != 200:
            return False

        if not ResponseValidator.validate_content_type(response):
            return False

        if not ResponseValidator.validate_json_response(response):
            return False

        updated_book = response.json()

        if not ResponseValidator.validate_book_structure(updated_book):
            return False

        if expected_book_data:
            for field, expected_value in expected_book_data.items():
                if field in updated_book and updated_book[field] != expected_value:
                    return False

        return True

    @staticmethod
    def validate_crud_operation_success(operation: str, response: Response) -> bool:
        """
        Validate CRUD operation response based on operation type.

        Args:
            operation: Type of operation ('create', 'read', 'update', 'delete')
            response: HTTP response object

        Returns:
            True if operation response is valid
        """
        operation_validators = {
            "create": lambda r: r.status_code == 200
            and ResponseValidator.validate_json_response(r),
            "read": lambda r: r.status_code in [200, 404]
            and (r.status_code == 404 or ResponseValidator.validate_json_response(r)),
            "update": lambda r: ResponseValidator.validate_update_response(r),
            "delete": lambda r: ResponseValidator.validate_delete_response(r),
        }

        from typing import Callable

        validator: Optional[Callable[[Response], bool]] = operation_validators.get(
            operation.lower()
        )
        if validator:
            return validator(response)

        return False

    @staticmethod
    def get_validation_errors(
        response: Response, expected_status: int = 200
    ) -> List[str]:
        """
        Get list of validation errors for a response.

        Args:
            response: HTTP response object
            expected_status: Expected status code

        Returns:
            List of validation error messages
        """
        errors = []

        if not ResponseValidator.validate_status_code(response, expected_status):
            errors.append(
                f"Expected status {expected_status}, got {response.status_code}"
            )

        if expected_status == 200:
            if not ResponseValidator.validate_content_type(response):
                errors.append("Expected JSON content type")

            if not ResponseValidator.validate_json_response(response):
                errors.append("Response is not valid JSON")

        return errors
