# Chicago Crime Big Data Pipeline

## Project Overview
For this project, I built a big data pipeline using MongoDB to analyze crime data from Chicago. The goal was to look at crime trends over time, figure out which districts have the most activity, and see what types of crimes happen the most.



## Platform Chosen and Why
I used MongoDB because it handles large datasets really well and doesn’t require a strict structure. The crime data has a lot of fields and can be messy, so MongoDB made it easier to store and work with. It also supports indexing and aggregation, which helped with performance when running queries.



## Dataset Description
The dataset comes from the City of Chicago Data Portal and includes millions of crime records.

Some of the main fields are:
- Date and time of the crime  
- Crime type and description  
- Location description  
- Whether an arrest was made  
- District and ward  
- Latitude and longitude  

Because of the size and detail of the dataset, it worked well for a big data project.



## Architecture
The pipeline follows this flow:

Chicago Crime CSV  
→ Python ingestion script  
→ MongoDB (crime_raw)  
→ Cleaning and validation  
→ MongoDB (crime_clean)  
→ Aggregations  
→ MongoDB (aggregated collections)  
→ Streamlit dashboard  



## Setup Instructions
Run these commands from the project folder:

docker compose up -d
docker ps

PYTHONPATH=. uv run python src/ingest_raw.py
PYTHONPATH=. uv run python src/clean_data.py
PYTHONPATH=. uv run python src/create_indexes.py
PYTHONPATH=. uv run python src/aggregate_data.py
PYTHONPATH=. uv run streamlit run src/app.py



## Pipeline Stages

### Raw Layer
The raw data is loaded from the CSV file into MongoDB and stored in the `crime_raw` collection. This keeps the original dataset unchanged.

### Clean Layer
The data is cleaned using Python and Pydantic. This includes handling missing values, standardizing text, converting dates, and removing duplicates. The cleaned data is stored in the `crime_clean` collection.

### Aggregated Layer
After cleaning, I created aggregated datasets to make analysis easier. These include:
- Crime trends over time  
- Crime by district  
- Most common crime types  

These are stored in separate collections and used for the dashboard.



## Team Members
Nicolas Radimer
