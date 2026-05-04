/*  # Chicago Crime Big Data Pipeline

## Project Overview
This project builds a big data pipeline using MongoDB to analyze Chicago crime data. The goal is to understand crime trends over time, identify high-crime districts, and analyze the most common crime types.

---

## Platform Chosen and Why
MongoDB was chosen because it can handle large datasets and supports flexible document-based storage. It also allows efficient querying through indexing and aggregation pipelines, which makes it a good fit for this type of data.

---

## Dataset Description
The dataset used is the Chicago Crimes dataset from the City of Chicago Data Portal.

It includes:
- Date and time of crime  
- Crime type and description  
- Location description  
- Arrest status  
- District and ward  
- Latitude and longitude  

The dataset contains millions of rows, making it suitable for a big data project.

---

## Architecture


Pipeline Flow:

Chicago Crime CSV  
→ Python Ingestion  
→ MongoDB (crime_raw)  
→ Cleaning + Validation  
→ MongoDB (crime_clean)  
→ Aggregations  
→ MongoDB (aggregated collections)  
→ Streamlit Dashboard  

---

## Setup Instructions

Run the following commands:

```bash
docker compose up -d
uv run python src/ingest_raw.py
uv run python src/clean_data.py
uv run python src/create_indexes.py
uv run python src/aggregate_data.py
uv run streamlit run src/app.py


## Pipeline Stages

##Raw Layer

Data is ingested from the CSV file into MongoDB and stored in the crime_raw collection.

##Clean Layer

Data is cleaned and validated using Python and Pydantic. This includes handling missing values, normalizing text, converting date formats, and removing duplicates. The cleaned data is stored in crime_clean.

##Aggregated Layer

Three aggregated datasets are created:

Crime trends over time
Crime by district
Most common crime types

These are stored in separate MongoDB collections and used for visualization. 


##Team Members
Nicolas Radimer 


