import logging
from datetime import datetime
from typing import Any

from pymongo import MongoClient
from tqdm import tqdm

from src.config import CLEAN_COLLECTION, DATABASE_NAME, MONGO_URI, RAW_COLLECTION
from src.models import CrimeRecord


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

BAD_RECORD_LOG = "logs/bad_records.log"


VIOLENT_CRIMES = {
    "homicide",
    "assault",
    "battery",
    "robbery",
    "criminal sexual assault",
}


def normalize_text(value: Any) -> str:
    if value is None:
        return "unknown"

    text = str(value).strip().lower()

    if text == "" or text == "nan":
        return "unknown"

    return text


def parse_date(value: Any) -> datetime | None:
    try:
        return datetime.strptime(str(value), "%m/%d/%Y %I:%M:%S %p")
    except Exception:
        return None


def clean_record(raw: dict[str, Any]) -> dict[str, Any] | None:
    date_value = parse_date(raw.get("Date"))

    if date_value is None:
        return None

    primary_type = normalize_text(raw.get("Primary Type"))
    description = normalize_text(raw.get("Description"))
    location_description = normalize_text(raw.get("Location Description"))

    case_number = normalize_text(raw.get("Case Number"))
    district = normalize_text(raw.get("District"))

    if case_number == "unknown":
        return None

    cleaned = {
        "case_number": case_number,
        "date": date_value,
        "primary_type": primary_type,
        "description": description,
        "location_description": location_description,
        "arrest": bool(raw.get("Arrest")),
        "domestic": bool(raw.get("Domestic")),
        "district": district,
        "ward": normalize_text(raw.get("Ward")),
        "latitude": raw.get("Latitude"),
        "longitude": raw.get("Longitude"),
        "crime_month": date_value.strftime("%Y-%m"),
        "crime_hour": date_value.hour,
        "is_violent_crime": primary_type in VIOLENT_CRIMES,
    }

    try:
        validated = CrimeRecord(**cleaned)
        return validated.model_dump()
    except Exception as error:
        with open(BAD_RECORD_LOG, "a") as file:
            file.write(f"{error} | {raw}\n")
        return None


def clean_data() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    raw_collection = db[RAW_COLLECTION]
    clean_collection = db[CLEAN_COLLECTION]

    clean_collection.drop()

    logging.info("Starting cleaning process")

    seen_case_numbers = set()
    clean_batch = []
    total_cleaned = 0
    total_skipped = 0

    cursor = raw_collection.find({}, no_cursor_timeout=True)

    for raw_record in tqdm(cursor):
        case_number = raw_record.get("Case Number")

        if case_number in seen_case_numbers:
            total_skipped += 1
            continue

        seen_case_numbers.add(case_number)

        cleaned = clean_record(raw_record)

        if cleaned is None:
            total_skipped += 1
            continue

        clean_batch.append(cleaned)

        if len(clean_batch) >= 10_000:
            clean_collection.insert_many(clean_batch)
            total_cleaned += len(clean_batch)
            clean_batch = []

    if clean_batch:
        clean_collection.insert_many(clean_batch)
        total_cleaned += len(clean_batch)

    logging.info(f"Cleaning complete. Cleaned: {total_cleaned}. Skipped: {total_skipped}")

    print(f"Clean rows inserted: {clean_collection.count_documents({})}")
    print(f"Skipped rows: {total_skipped}")


if __name__ == "__main__":
    clean_data()