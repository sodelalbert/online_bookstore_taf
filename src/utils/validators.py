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
        "Validating response status code: %s, expected: %s",
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
    Validate JSON data against a given schema.
    """

    logging.info("Validating JSON against schema")
    logging.info("  JSON data: %s", json_data)
    logging.info("  Schema: %s", schema)

    json_validate(instance=json_data, schema=schema)

    logging.info("JSON validation successful")
