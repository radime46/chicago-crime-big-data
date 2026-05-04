import logging

from pymongo import MongoClient

from config import (
    AGG_DISTRICT_COLLECTION,
    AGG_MONTHLY_COLLECTION,
    AGG_TYPE_COLLECTION,
    CLEAN_COLLECTION,
    DATABASE_NAME,
    MONGO_URI,
)


logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def aggregate_monthly_crime(db) -> None:
    result = db[CLEAN_COLLECTION].aggregate(
        [
            {
                "$group": {
                    "_id": "$crime_month",
                    "crime_count": {"$sum": 1},
                    "violent_crime_count": {
                        "$sum": {"$cond": ["$is_violent_crime", 1, 0]}
                    },
                    "arrest_count": {
                        "$sum": {"$cond": ["$arrest", 1, 0]}
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]
    )

    docs = [
        {
            "crime_month": row["_id"],
            "crime_count": row["crime_count"],
            "violent_crime_count": row["violent_crime_count"],
            "arrest_count": row["arrest_count"],
        }
        for row in result
    ]

    db[AGG_MONTHLY_COLLECTION].drop()
    if docs:
        db[AGG_MONTHLY_COLLECTION].insert_many(docs)


def aggregate_by_district(db) -> None:
    result = db[CLEAN_COLLECTION].aggregate(
        [
            {
                "$group": {
                    "_id": "$district",
                    "crime_count": {"$sum": 1},
                    "violent_crime_count": {
                        "$sum": {"$cond": ["$is_violent_crime", 1, 0]}
                    },
                }
            },
            {"$sort": {"crime_count": -1}},
        ]
    )

    docs = [
        {
            "district": row["_id"],
            "crime_count": row["crime_count"],
            "violent_crime_count": row["violent_crime_count"],
        }
        for row in result
    ]

    db[AGG_DISTRICT_COLLECTION].drop()
    if docs:
        db[AGG_DISTRICT_COLLECTION].insert_many(docs)


def aggregate_by_crime_type(db) -> None:
    result = db[CLEAN_COLLECTION].aggregate(
        [
            {
                "$group": {
                    "_id": "$primary_type",
                    "crime_count": {"$sum": 1},
                    "arrest_count": {
                        "$sum": {"$cond": ["$arrest", 1, 0]}
                    },
                }
            },
            {"$sort": {"crime_count": -1}},
            {"$limit": 15},
        ]
    )

    docs = [
        {
            "primary_type": row["_id"],
            "crime_count": row["crime_count"],
            "arrest_count": row["arrest_count"],
        }
        for row in result
    ]

    db[AGG_TYPE_COLLECTION].drop()
    if docs:
        db[AGG_TYPE_COLLECTION].insert_many(docs)


def run_aggregations() -> None:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    logging.info("Starting aggregations")

    aggregate_monthly_crime(db)
    aggregate_by_district(db)
    aggregate_by_crime_type(db)

    logging.info("Finished aggregations")

    print("Aggregations created successfully")


if __name__ == "__main__":
    run_aggregations()