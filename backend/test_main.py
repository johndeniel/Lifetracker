import pytest
from datetime import date
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Define a fixture to provide a fixed current date for testing
@pytest.fixture
def fixed_current_date():
    return date(2024, 1, 1)


# Test case for calculating age with a valid birth date
@pytest.mark.parametrize(
    "data, expected_status, expected_days",
    [
        (
            {"month": 5, "day": 15, "year": 1990},
            200,
            12371,
        )  # Calculate the expected number of days
    ],
)
def test_calculate_age_valid(data, expected_status, expected_days, fixed_current_date):
    """
    Test calculation of age with a valid birth date.
    """
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status
    if expected_days is not None:
        expected_message = f"You are {expected_days} days old"
        assert response.json()["message"] == expected_message


# Test case for handling invalid birth dates
@pytest.mark.parametrize(
    "data, expected_status",
    [
        ({"month": 13, "day": 32, "year": 2025}, 200),  # Invalid month and day
        ({"month": 2, "day": 29, "year": 2021}, 200),  # Invalid date for non-leap year
        ({"month": 2, "day": 30, "year": 2000}, 200),  # Invalid day for February
    ],
)
def test_calculate_age_invalid(data, expected_status, fixed_current_date):
    """
    Test handling of invalid birth dates.
    """
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status
    assert response.json()["message"] == "Invalid birth date"


# Test case for rendering HTML form
def test_render_form():
    """
    Test rendering of HTML form.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<form" in response.content
