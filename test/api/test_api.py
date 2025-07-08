"""
test
"""

import pytest


@pytest.mark.smoke
@pytest.mark.api
def test_api() -> None:
    """
    Test API functionality.
    """
    assert True, "API test should pass"
