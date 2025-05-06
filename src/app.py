import logging
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.__init__ import create_app

store_dict = create_app()
app = FastAPI()


@app.get("/")
def visit(store_name: str, year: int, month: int, day: int, hour: int) -> JSONResponse:
    # If the store is not in the dictionary
    if not (store_name in store_dict.keys()):
        return JSONResponse(status_code=404, content="Store Not Found")

    # Check the year
    if year < 2020:
        return JSONResponse(status_code=404, content="No data before 2020")

    # Check the date
    try:
        requested_date = date(year, month, day)
    except ValueError as e:
        logging.error(f"Could not cast date: {e}")
        return JSONResponse(status_code=404, content="Enter a valid date")

    # Check if the date is in the past
    if date.today() < requested_date:
        return JSONResponse(status_code=404, content="Choose a date in the past")

    if hour < 0 or hour > 23:
        return JSONResponse(status_code=404, content="Enter a valid hour")

    return JSONResponse(
        status_code=200,
        content=store_dict[f"{store_name}"].get_visit_count(
            date(year=year, month=month, day=day), business_hour=hour
        ),
    )
