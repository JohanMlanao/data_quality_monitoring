import logging
from datetime import date

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.__init__ import create_app

store_dict = create_app()
app = FastAPI()


@app.get("/")
def visit(
    store_name: str, year: int, month: int, day: int, sensor_id: int | None = None
) -> JSONResponse:
    # If the store is not in the dictionary
    if not (store_name in store_dict.keys()):
        return JSONResponse(status_code=404, content="Store Not Found")

    # Check the value of sensor_id
    if sensor_id and (sensor_id > 7 or sensor_id < 0):
        return JSONResponse(
            status_code=404, content="Sensor_id should be between 0 and 7"
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
        visit_count = store_dict[store_name].get_all_traffic(
            date(year=year, month=month, day=day)
        )
    else:
        visit_count = store_dict[store_name].get_sensor_traffic(
            sensor_id, date(year=year, month=month, day=day)
        )
    if visit_count < 0:
        return JSONResponse(
            status_code=404, content="The store was closed try another date"
        )

    return JSONResponse(status_code=200, content=visit_count)
