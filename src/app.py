import pandas as pd
import streamlit as st
from pymongo import MongoClient

from config import (
    AGG_DISTRICT_COLLECTION,
    AGG_MONTHLY_COLLECTION,
    AGG_TYPE_COLLECTION,
    DATABASE_NAME,
    MONGO_URI,
)


st.set_page_config(page_title="Chicago Crime Dashboard", layout="wide")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def load_collection(collection_name: str) -> pd.DataFrame:
    data = list(db[collection_name].find({}, {"_id": 0}))
    return pd.DataFrame(data)


st.title("Chicago Crime Big Data Dashboard")

st.write(
    "This dashboard uses aggregated data stored in MongoDB. "
    "It shows crime trends over time, high-crime districts, and common crime types."
)


# Load data
monthly_df = load_collection(AGG_MONTHLY_COLLECTION)
district_df = load_collection(AGG_DISTRICT_COLLECTION)
type_df = load_collection(AGG_TYPE_COLLECTION)


# Chart 1: Crime over time
st.header("1. Crime Trend Over Time")
st.write("Business Question: How does crime change over time?")
st.line_chart(
    monthly_df.set_index("crime_month")[["crime_count", "violent_crime_count"]]
)


# Chart 2: Crime by district
st.header("2. Crime by District")
st.write("Business Question: Which districts have the highest crime volume?")
district_chart = district_df.head(15).set_index("district")[["crime_count"]]
st.bar_chart(district_chart)


# Chart 3: Crime types
st.header("3. Top Crime Types")
st.write("Business Question: What are the most common types of crime?")
type_chart = type_df.set_index("primary_type")[["crime_count"]]