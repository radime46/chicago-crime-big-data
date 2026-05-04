import logging
from pathlib import Path

import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm

from config import DATABASE_NAME, MONGO_URI, RAW_COLLECTION


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DATA_FILE = Path("data/raw/chicago_crime.csv")


def ingest_raw_data() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[RAW_COLLECTION]

    collection.drop()

    logging.info("Starting raw data ingestion")

    chunk_size = 50_000
    total_inserted = 0

    for chunk in tqdm(pd.read_csv(DATA_FILE, chunksize=chunk_size)):
        records = chunk.to_dict("records")
        collection.insert_many(records)
        total_inserted += len(records)

    logging.info(f"Finished raw ingestion. Total rows inserted: {total_inserted}")

    print(f"Raw rows inserted: {collection.count_documents({})}")


if __name__ == "__main__":
    ingest_raw_data()