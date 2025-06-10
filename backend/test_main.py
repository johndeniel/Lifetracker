import pytest
from datetime import date, datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# Fixtures
@pytest.fixture
def fixed_current_date():
    return date(2024, 1, 1)

@pytest.fixture
def mock_current_date():
    """Mock datetime.date.today() to return a fixed date"""
    with patch('main.date') as mock_date:
        mock_date.today.return_value = date(2024, 1, 1)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        yield mock_date

# Helper function to calculate expected days
def calculate_expected_days(birth_year, birth_month, birth_day, current_date=date(2024, 1, 1)):
    birth_date = date(birth_year, birth_month, birth_day)
    return (current_date - birth_date).days

# Valid Birth Date Tests
@pytest.mark.parametrize(
    "data, expected_status, description",
    [
        # Recent births
        ({"month": 12, "day": 31, "year": 2023}, 200, "Born yesterday"),
        ({"month": 12, "day": 30, "year": 2023}, 200, "Born 2 days ago"),
        ({"month": 1, "day": 1, "year": 2024}, 200, "Born today"),
        
        # Various ages
        ({"month": 1, "day": 1, "year": 2023}, 200, "Exactly 1 year old"),
        ({"month": 1, "day": 1, "year": 2020}, 200, "4 years old"),
        ({"month": 1, "day": 1, "year": 2010}, 200, "14 years old"),
        ({"month": 1, "day": 1, "year": 2000}, 200, "24 years old"),
        ({"month": 1, "day": 1, "year": 1990}, 200, "34 years old"),
        ({"month": 1, "day": 1, "year": 1980}, 200, "44 years old"),
        ({"month": 1, "day": 1, "year": 1970}, 200, "54 years old"),
        ({"month": 1, "day": 1, "year": 1960}, 200, "64 years old"),
        ({"month": 1, "day": 1, "year": 1950}, 200, "74 years old"),
        ({"month": 1, "day": 1, "year": 1940}, 200, "84 years old"),
        ({"month": 1, "day": 1, "year": 1930}, 200, "94 years old"),
        ({"month": 1, "day": 1, "year": 1920}, 200, "104 years old"),
        
        # Different months
        ({"month": 2, "day": 15, "year": 2020}, 200, "February birth"),
        ({"month": 3, "day": 20, "year": 2020}, 200, "March birth"),
        ({"month": 4, "day": 10, "year": 2020}, 200, "April birth"),
        ({"month": 5, "day": 5, "year": 2020}, 200, "May birth"),
        ({"month": 6, "day": 25, "year": 2020}, 200, "June birth"),
        ({"month": 7, "day": 4, "year": 2020}, 200, "July 4th birth"),
        ({"month": 8, "day": 31, "year": 2020}, 200, "August birth"),
        ({"month": 9, "day": 15, "year": 2020}, 200, "September birth"),
        ({"month": 10, "day": 31, "year": 2020}, 200, "Halloween birth"),
        ({"month": 11, "day": 11, "year": 2020}, 200, "Veterans Day birth"),
        ({"month": 12, "day": 25, "year": 2020}, 200, "Christmas birth"),
        
        # Leap year births
        ({"month": 2, "day": 29, "year": 2020}, 200, "Leap day 2020"),
        ({"month": 2, "day": 29, "year": 2016}, 200, "Leap day 2016"),
        ({"month": 2, "day": 29, "year": 2012}, 200, "Leap day 2012"),
        ({"month": 2, "day": 29, "year": 2000}, 200, "Leap day 2000"),
        
        # Month boundaries
        ({"month": 1, "day": 31, "year": 2020}, 200, "End of January"),
        ({"month": 3, "day": 31, "year": 2020}, 200, "End of March"),
        ({"month": 4, "day": 30, "year": 2020}, 200, "End of April"),
        ({"month": 5, "day": 31, "year": 2020}, 200, "End of May"),
        ({"month": 6, "day": 30, "year": 2020}, 200, "End of June"),
        ({"month": 7, "day": 31, "year": 2020}, 200, "End of July"),
        ({"month": 8, "day": 31, "year": 2020}, 200, "End of August"),
        ({"month": 9, "day": 30, "year": 2020}, 200, "End of September"),
        ({"month": 10, "day": 31, "year": 2020}, 200, "End of October"),
        ({"month": 11, "day": 30, "year": 2020}, 200, "End of November"),
        ({"month": 12, "day": 31, "year": 2020}, 200, "End of December"),
        
        # Start of months
        ({"month": 2, "day": 1, "year": 2020}, 200, "Start of February"),
        ({"month": 3, "day": 1, "year": 2020}, 200, "Start of March"),
        ({"month": 4, "day": 1, "year": 2020}, 200, "Start of April"),
        ({"month": 5, "day": 1, "year": 2020}, 200, "Start of May"),
        ({"month": 6, "day": 1, "year": 2020}, 200, "Start of June"),
        ({"month": 7, "day": 1, "year": 2020}, 200, "Start of July"),
        ({"month": 8, "day": 1, "year": 2020}, 200, "Start of August"),
        ({"month": 9, "day": 1, "year": 2020}, 200, "Start of September"),
        ({"month": 10, "day": 1, "year": 2020}, 200, "Start of October"),
        ({"month": 11, "day": 1, "year": 2020}, 200, "Start of November"),
        ({"month": 12, "day": 1, "year": 2020}, 200, "Start of December"),
    ],
)
def test_calculate_age_valid_comprehensive(data, expected_status, description, mock_current_date):
    """Test calculation of age with valid birth dates - comprehensive scenarios"""
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status
    
    expected_days = calculate_expected_days(data["year"], data["month"], data["day"])
    expected_message = f"You are {expected_days} days old"
    assert response.json()["message"] == expected_message

# Invalid Birth Date Tests
@pytest.mark.parametrize(
    "data, expected_status, description",
    [
        # Invalid months
        ({"month": 0, "day": 15, "year": 2020}, 200, "Month 0"),
        ({"month": 13, "day": 15, "year": 2020}, 200, "Month 13"),
        ({"month": 14, "day": 15, "year": 2020}, 200, "Month 14"),
        ({"month": 100, "day": 15, "year": 2020}, 200, "Month 100"),
        ({"month": -1, "day": 15, "year": 2020}, 200, "Negative month"),
        ({"month": -10, "day": 15, "year": 2020}, 200, "Very negative month"),
        
        # Invalid days
        ({"month": 1, "day": 0, "year": 2020}, 200, "Day 0"),
        ({"month": 1, "day": 32, "year": 2020}, 200, "Day 32 in January"),
        ({"month": 2, "day": 30, "year": 2020}, 200, "Day 30 in February"),
        ({"month": 2, "day": 31, "year": 2020}, 200, "Day 31 in February"),
        ({"month": 4, "day": 31, "year": 2020}, 200, "Day 31 in April"),
        ({"month": 6, "day": 31, "year": 2020}, 200, "Day 31 in June"),
        ({"month": 9, "day": 31, "year": 2020}, 200, "Day 31 in September"),
        ({"month": 11, "day": 31, "year": 2020}, 200, "Day 31 in November"),
        ({"month": 1, "day": -1, "year": 2020}, 200, "Negative day"),
        ({"month": 1, "day": 100, "year": 2020}, 200, "Day 100"),
        
        # Non-leap year February 29th
        ({"month": 2, "day": 29, "year": 2021}, 200, "Feb 29 in non-leap year 2021"),
        ({"month": 2, "day": 29, "year": 2022}, 200, "Feb 29 in non-leap year 2022"),
        ({"month": 2, "day": 29, "year": 2023}, 200, "Feb 29 in non-leap year 2023"),
        ({"month": 2, "day": 29, "year": 1900}, 200, "Feb 29 in 1900 (not leap)"),
        ({"month": 2, "day": 29, "year": 2100}, 200, "Feb 29 in 2100 (not leap)"),
        
        # Future dates
        ({"month": 1, "day": 2, "year": 2024}, 200, "Future date - tomorrow"),
        ({"month": 2, "day": 1, "year": 2024}, 200, "Future date - next month"),
        ({"month": 1, "day": 1, "year": 2025}, 200, "Future date - next year"),
        ({"month": 12, "day": 31, "year": 2025}, 200, "Future date - far future"),
        
        # Combined invalid values
        ({"month": 13, "day": 32, "year": 2025}, 200, "Invalid month and day"),
        ({"month": 0, "day": 0, "year": 2020}, 200, "Zero month and day"),
        ({"month": -1, "day": -1, "year": 2020}, 200, "Negative month and day"),
        ({"month": 15, "day": 50, "year": 2030}, 200, "Very invalid month and day"),
    ],
)
def test_calculate_age_invalid_comprehensive(data, expected_status, description, mock_current_date):
    """Test handling of invalid birth dates - comprehensive scenarios"""
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status
    assert response.json()["message"] == "Invalid birth date"

# Edge Case Tests
@pytest.mark.parametrize(
    "data, expected_status, description",
    [
        # Extreme years
        ({"month": 1, "day": 1, "year": 1900}, 200, "Very old person - 1900"),
        ({"month": 1, "day": 1, "year": 1800}, 200, "Extremely old - 1800"),
        ({"month": 1, "day": 1, "year": 1000}, 200, "Medieval times"),
        ({"month": 1, "day": 1, "year": 1}, 200, "Year 1 AD"),
        ({"month": 1, "day": 1, "year": 0}, 200, "Year 0"),
        
        # Century boundaries
        ({"month": 1, "day": 1, "year": 2000}, 200, "Y2K baby"),
        ({"month": 12, "day": 31, "year": 1999}, 200, "Last day of millennium"),
        
        # Leap year edge cases
        ({"month": 2, "day": 28, "year": 2020}, 200, "Day before leap day"),
        ({"month": 3, "day": 1, "year": 2020}, 200, "Day after leap day"),
        
        # Various year patterns
        ({"month": 6, "day": 15, "year": 2004}, 200, "Leap year 2004"),
        ({"month": 6, "day": 15, "year": 2008}, 200, "Leap year 2008"),
        ({"month": 6, "day": 15, "year": 1996}, 200, "Leap year 1996"),
        ({"month": 6, "day": 15, "year": 1992}, 200, "Leap year 1992"),
    ],
)
def test_calculate_age_edge_cases(data, expected_status, description, mock_current_date):
    """Test edge cases for age calculation"""
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status
    
    if expected_status == 200:
        try:
            expected_days = calculate_expected_days(data["year"], data["month"], data["day"])
            expected_message = f"You are {expected_days} days old"
            assert response.json()["message"] == expected_message
        except ValueError:
            # Invalid date should return error message
            assert response.json()["message"] == "Invalid birth date"

# Input Validation Tests
@pytest.mark.parametrize(
    "data, expected_status, description",
    [
        # Missing fields
        ({"month": 5, "day": 15}, 422, "Missing year"),
        ({"month": 5, "year": 2020}, 422, "Missing day"),
        ({"day": 15, "year": 2020}, 422, "Missing month"),
        ({}, 422, "Missing all fields"),
        ({"month": 5}, 422, "Only month provided"),
        ({"day": 15}, 422, "Only day provided"),
        ({"year": 2020}, 422, "Only year provided"),
        
        # Wrong data types
        ({"month": "5", "day": 15, "year": 2020}, 422, "String month"),
        ({"month": 5, "day": "15", "year": 2020}, 422, "String day"),
        ({"month": 5, "day": 15, "year": "2020"}, 422, "String year"),
        ({"month": 5.5, "day": 15, "year": 2020}, 422, "Float month"),
        ({"month": 5, "day": 15.5, "year": 2020}, 422, "Float day"),
        ({"month": 5, "day": 15, "year": 2020.5}, 422, "Float year"),
        ({"month": None, "day": 15, "year": 2020}, 422, "None month"),
        ({"month": 5, "day": None, "year": 2020}, 422, "None day"),
        ({"month": 5, "day": 15, "year": None}, 422, "None year"),
        
        # Extra fields
        ({"month": 5, "day": 15, "year": 2020, "extra": "field"}, 200, "Extra field should be ignored"),
        ({"month": 5, "day": 15, "year": 2020, "hour": 12}, 200, "Extra hour field"),
    ],
)
def test_input_validation(data, expected_status, description, mock_current_date):
    """Test input validation and error handling"""
    response = client.post("/calculate/", json=data)
    assert response.status_code == expected_status

# Malformed Request Tests
def test_malformed_json():
    """Test handling of malformed JSON"""
    response = client.post("/calculate/", data="invalid json")
    assert response.status_code == 422

def test_empty_request():
    """Test handling of empty request body"""
    response = client.post("/calculate/")
    assert response.status_code == 422

def test_non_json_content_type():
    """Test handling of non-JSON content type"""
    response = client.post("/calculate/", data="month=5&day=15&year=2020")
    assert response.status_code == 422

# Response Format Tests
def test_response_format_valid(mock_current_date):
    """Test that response format is correct for valid dates"""
    data = {"month": 1, "day": 1, "year": 2020}
    response = client.post("/calculate/", json=data)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert json_response["message"].startswith("You are ")
    assert json_response["message"].endswith(" days old")

def test_response_format_invalid(mock_current_date):
    """Test that response format is correct for invalid dates"""
    data = {"month": 13, "day": 32, "year": 2020}
    response = client.post("/calculate/", json=data)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response
    assert json_response["message"] == "Invalid birth date"

# HTML Form Tests
def test_render_form_comprehensive():
    """Test comprehensive HTML form rendering"""
    response = client.get("/")
    
    assert response.status_code == 200
    content = response.content.decode()
    
    # Check for form elements
    assert "<form" in content
    assert "</form>" in content
    assert "method=" in content
    assert "action=" in content
    
    # Check for input fields
    assert 'name="month"' in content or 'id="month"' in content
    assert 'name="day"' in content or 'id="day"' in content
    assert 'name="year"' in content or 'id="year"' in content
    
    # Check for submit button
    assert 'type="submit"' in content or '<button' in content

def test_form_content_type():
    """Test that form returns HTML content type"""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

# HTTP Method Tests
def test_get_calculate_endpoint():
    """Test GET request to calculate endpoint (should not be allowed)"""
    response = client.get("/calculate/")
    assert response.status_code == 405  # Method Not Allowed

def test_put_calculate_endpoint():
    """Test PUT request to calculate endpoint (should not be allowed)"""
    response = client.put("/calculate/", json={"month": 5, "day": 15, "year": 2020})
    assert response.status_code == 405  # Method Not Allowed

def test_delete_calculate_endpoint():
    """Test DELETE request to calculate endpoint (should not be allowed)"""
    response = client.delete("/calculate/")
    assert response.status_code == 405  # Method Not Allowed

# Concurrent Request Tests
def test_multiple_requests_same_data(mock_current_date):
    """Test multiple requests with same data return consistent results"""
    data = {"month": 5, "day": 15, "year": 2020}
    
    responses = []
    for _ in range(5):
        response = client.post("/calculate/", json=data)
        responses.append(response)
    
    # All responses should be identical
    first_response = responses[0]
    for response in responses[1:]:
        assert response.status_code == first_response.status_code
        assert response.json() == first_response.json()

# Performance Tests
def test_large_year_values(mock_current_date):
    """Test handling of very large year values"""
    test_cases = [
        {"month": 1, "day": 1, "year": 9999},
        {"month": 1, "day": 1, "year": 99999},
        {"month": 1, "day": 1, "year": 999999},
    ]
    
    for data in test_cases:
        response = client.post("/calculate/", json=data)
        assert response.status_code == 200
        # Should handle gracefully (either calculate or return invalid date)

def test_negative_year_values(mock_current_date):
    """Test handling of negative year values"""
    test_cases = [
        {"month": 1, "day": 1, "year": -1},
        {"month": 1, "day": 1, "year": -100},
        {"month": 1, "day": 1, "year": -2024},
    ]
    
    for data in test_cases:
        response = client.post("/calculate/", json=data)
        assert response.status_code == 200
        # Should handle gracefully

# Boundary Value Tests
@pytest.mark.parametrize(
    "data, description",
    [
        ({"month": 1, "day": 1, "year": 2023}, "Minimum valid date in 2023"),
        ({"month": 12, "day": 31, "year": 2023}, "Maximum valid date in 2023"),
        ({"month": 2, "day": 28, "year": 2023}, "Last day of February non-leap"),
        ({"month": 2, "day": 29, "year": 2024}, "Last day of February leap year"),
    ]
)
def test_boundary_values(data, description, mock_current_date):
    """Test boundary value analysis"""
    response = client.post("/calculate/", json=data)
    assert response.status_code == 200
    
    expected_days = calculate_expected_days(data["year"], data["month"], data["day"])
    expected_message = f"You are {expected_days} days old"
    assert response.json()["message"] == expected_message

# Integration Tests
def test_end_to_end_workflow():
    """Test complete end-to-end workflow"""
    # First, get the form
    form_response = client.get("/")
    assert form_response.status_code == 200
    
    # Then, submit a calculation
    calc_response = client.post("/calculate/", json={"month": 6, "day": 15, "year": 2000})
    assert calc_response.status_code == 200
    assert "days old" in calc_response.json()["message"]

# Error Recovery Tests
def test_malformed_then_valid_request(mock_current_date):
    """Test that app recovers from malformed request"""
    # First, send malformed request
    malformed_response = client.post("/calculate/", data="invalid")
    assert malformed_response.status_code == 422
    
    # Then, send valid request
    valid_response = client.post("/calculate/", json={"month": 6, "day": 15, "year": 2000})
    assert valid_response.status_code == 200
    assert "days old" in valid_response.json()["message"]
