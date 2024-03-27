from fastapi.testclient import TestClient
from main import app

# Initialize a test client for the FastAPI application
client = TestClient(app)

def test_calculate_age_valid_input():
    # Test case for valid input
    response = client.post("/calculate/", json={"month": 1, "day": 1, "year": 2000})
    assert response.status_code == 200
    assert "You are" in response.json()["message"]  # Check if message contains expected text

def test_calculate_age_invalid_input():
    # Test case for invalid input (invalid date)
    response = client.post("/calculate/", json={"month": 13, "day": 32, "year": 2023})
    assert response.status_code == 422  # Expecting status code 422 for validation error
    assert response.json()["detail"][0]["msg"] == "value is not a valid date"  # Check for expected validation error message

    # Test case for invalid input (missing required fields)
    response = client.post("/calculate/", json={"month": 1, "day": 1})  # Missing "year"
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"  # Check for expected validation error message

    # Add more test cases as needed...

# You can add more test cases as needed to cover different scenarios
    
# To run the test locally, use the following command:
# pytest test_main.py