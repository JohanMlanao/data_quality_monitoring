import logging
import sys
from datetime import date

year, month, day = [int(v) for v in sys.argv[1].split("-")]
try:
    requested_date = date(year=year, month=month, day=day)
    print(requested_date)
except ValueError as e:
    logging.error(f"Could not cast date: {e}")
