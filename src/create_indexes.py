from pymongo import MongoClient

from config import CLEAN_COLLECTION, DATABASE_NAME, MONGO_URI


def create_indexes() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[CLEAN_COLLECTION]

    # Create indexes
    collection.create_index("date")
    collection.create_index("crime_month")
    collection.create_index("district")
    collection.create_index("primary_type")
    collection.create_index("is_violent_crime")

    print("Indexes created successfully")


if __name__ == "__main__":
    create_indexes()