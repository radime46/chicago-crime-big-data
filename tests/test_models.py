from datetime import datetime
from src.models import CrimeRecord


def test_crime_record_model():
    record = CrimeRecord(
        case_number="123",
        date=datetime.now(),
        primary_type="battery",
        description="simple",
        location_description="street",
        arrest=True,
        domestic=False,
        district="1",
        ward="2",
        latitude=41.0,
        longitude=-87.0,
        crime_month="2024-01",
        crime_hour=12,
        is_violent_crime=True,
    )

    assert record.primary_type == "battery"