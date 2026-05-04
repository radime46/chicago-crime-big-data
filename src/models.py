from datetime import datetime
from pydantic import BaseModel


class CrimeRecord(BaseModel):
    case_number: str
    date: datetime
    primary_type: str
    description: str
    location_description: str
    arrest: bool
    domestic: bool
    district: str
    ward: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    crime_month: str
    crime_hour: int
    is_violent_crime: bool