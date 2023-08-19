from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class RequestData(BaseModel):
    value1: int  # month
    value2: int  # day
    value3: int  # year

class ResponseData(BaseModel):
    message: str  

@app.post("/calculate/", response_model=ResponseData)
async def calculate_values(data: RequestData):
    try:
        birth_date = datetime(data.value3, data.value1, data.value2)
    except ValueError:
        return {"message": "Invalid birth date"}

    current_date = datetime.now()
    days_passed = (current_date - birth_date).days
    return {"message": f"You are {days_passed} days old"}

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


# uvicorn main:app --reload