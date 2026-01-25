# extra data tyles

'''
additional data types:
- UUID: universally unique identifier. string representation of a 128-bit value
- datetime.datetime: python standard library datetime class. string representation in ISO 8601 format. like: "2023-01-01T12:00:00"
- datetime.date: python standard library date class. string representation in ISO 8601 format. like: "2023-01-01"
- datetime.time: python standard library time class. string representation in ISO 8601 format. like: "12:00:00"
- timedelta: python standard library timedelta class. string representation in ISO 8601 time diff encoding.
- frozenset: immutable version of set. represented as a list in JSON.
- bytes: binary data. represented as base64 encoded string with binary format.
- decimal: high-precision decimal number. handle the same as float.
'''

## examples
from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI, Body

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()] ,
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_datetime
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }