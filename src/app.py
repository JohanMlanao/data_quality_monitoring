import logging
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.__init__ import create_app

store_dict = create_app()
app = FastAPI()


@app.get("/")
def visit(
    store_location: str, year: int, month: int, day: int, sensor_id: str | None = None
) -> JSONResponse:
    # If the store is not in the dictionary
    if not (store_location in store_dict.keys()):
        return JSONResponse(status_code=404, content="Store Not Found")

    # Check the value of sensor_id
    if sensor_id and (sensor_id not in ["A", "B", "C", "D"]):
        return JSONResponse(
            status_code=404, content="Sensor_id should be A, B, C or D"
        )

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

    # If no sensor choose return the visit for the whole store
    if sensor_id is None:
        visit_count = store_dict[store_location].get_all_traffic(
            date(year=year, month=month, day=day)
        )
    else:
        visit_count = store_dict[store_location].get_sensor_traffic(
            sensor_id, date(year=year, month=month, day=day)
        )

    return JSONResponse(status_code=200, content=visit_count)
