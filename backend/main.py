from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime, date

# Initialize FastAPI app
app = FastAPI()

# Initialize Jinja2Templates for HTML rendering
client = Jinja2Templates(directory="frontend")


class RequestData(BaseModel):
    """
    Pydantic model defining the structure of the request data expected
    by the API endpoint. This model contains three attributes representing
    the components of a date: month, day, and year.

    Attributes:
        month (int): An integer representing the month component of the date.
        day (int): An integer representing the day component of the date.
        year (int): An integer representing the year component of the date.
    """

    month: int
    day: int
    year: int


class ResponseData(BaseModel):
    """
    Pydantic model defining the structure of the response data returned
    by the API endpoint. This model contains a single attribute:

    Attributes:
        message (str): A string representing the message to be included
                       in the API response.
    """

    message: str


def get_current_date():
    """
    Dependency function to get the current date.

    Returns:
        date: The current date.
    """
    return date.today()


@app.post("/calculate/", response_model=ResponseData)
async def calculate_age(
    data: RequestData, current_date: date = Depends(get_current_date)
):
    """
    Endpoint to calculate the number of days passed since the provided birth date.

    Args:
        data (RequestData): The request data containing the birth date.
        current_date (date, optional): The current date. It is retrieved using the
                                        dependency function get_current_date.

    Returns:
        dict: A dictionary containing the number of days passed since the birth date
              or an error message if the provided date is invalid.
    """
    try:
        # Construct birth date from the provided data
        birth_date = datetime(data.year, data.month, data.day)
    except ValueError:
        # Return error message for invalid date input
        return {"message": "Invalid birth date"}

    # Calculate days passed since birth
    days_passed = (current_date - birth_date.date()).days

    # Return the result
    return {"message": f"You are {days_passed} days old"}


@app.get("/", response_class=HTMLResponse)
async def render_form(request: Request):
    """
    Endpoint to render the HTML form for providing the birth date.

    Args:
        request (Request): The incoming request.

    Returns:
        TemplateResponse: HTML template response rendering the form.
    """
    return client.TemplateResponse("index.html", {"request": request})


# To run the app locally, use the following command:
# uvicorn backend.main:app --reload
