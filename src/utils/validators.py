"""
Utility functions for validating API responses and JSON data.
"""

import logging
from jsonschema import validate as json_validate
from requests.models import Response


def validate_status_code(
    response: Response, expected_status_codes: int | list[int]
) -> None:
    """
    Validate that the response status code matches the expected value(s).
    """

    logging.info(
        "Received response status code: %s, expected: %s",
        response.status_code,
        expected_status_codes,
    )

    if isinstance(expected_status_codes, int):
        assert response.status_code == expected_status_codes
    else:
        assert response.status_code in expected_status_codes


def validate_content_type(response: Response, expected_content_type: str) -> None:
    """
    Validate that the response content type matches the expected value.
    """
    logging.info(
        "Validating response content type: %s, expected: %s",
        response.headers.get("content-type"),
        expected_content_type,
    )

    assert expected_content_type in response.headers.get("content-type", "")


def validate_json_schema(json_data: dict, schema: dict) -> None:
    """
    Validate JSON data against a given schema or Data.
    """

    logging.info("Validating JSON against schema")
    logging.info("  JSON data: %s", json_data)
    logging.info("  Schema: %s", schema)

    json_validate(instance=json_data, schema=schema)

    logging.info("JSON validation successful")


def validate_elapsed_time(response: Response, max_seconds: float) -> None:
    """
    Validate that the response time is within the acceptable limit.
    """
    elapsed_time = response.elapsed.total_seconds()
    logging.info(
        "Validating response time: %s seconds, max allowed: %s seconds",
        elapsed_time,
        max_seconds,
    )

    assert elapsed_time < max_seconds, f"Response took too long: {elapsed_time} seconds"


def validate_response_reason(response: Response, expected_reason: str) -> None:
    """
    Validate that the response reason matches the expected value.
    """
    logging.info(
        "Validating response reason: %s, expected: %s",
        response.reason,
        expected_reason,
    )

    assert (
        response.reason == expected_reason
    ), f"Expected reason '{expected_reason}', but got '{response.reason}'"
