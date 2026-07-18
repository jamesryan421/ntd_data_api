# Script to update local NTD database from API endpoints.

# Import third-party dependencies
import logging
import os
import urllib.parse
from dotenv import load_dotenv

# Import local package
from ntd_data_extractor.extractor import TransitDataPipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment and configuration parameters
load_dotenv()

# 1. Pull the raw components out of the environment
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")

# 2. Safely URL-encode the password (handles @, !, #, etc.)
safe_password = urllib.parse.quote_plus(password)

# 3. Assemble the string cleanly in your code
DB_CONNECTION = f"postgresql://{user}:{safe_password}@{host}:{port}/{db_name}"

endpoints_to_sync = {
    "annual_metrics":os.environ.get("API_ANNUAL_METRICS"),
    "monthly_ridership":os.environ.get("API_MONTHLY_RIDERSHIP"),
    "agency_info":os.environ.get("API_AGENCY_INFO"),
    "stations_facilities_type":os.environ.get("API_STATIONS_FACILITIES_TYPE"),
    "stations_facilities_mode_age":os.environ.get("API_STATIONS_FACILITIES_MODE_AGE"),
    "vehicles_age":os.environ.get("API_VEHICLE_AGE"),
    "vehicles_type":os.environ.get("API_VEHICLES_TYPE")
}

def main():
    # If the .env file is missing or broken, stop execution immediately before erroring out
    if not DB_CONNECTION:
        #raise ValueError("❌ Critical Error: DB_CONNECTION variable not found. Check your .env file.")
        logging.error(f"Critical Error: DB_CONNECTION variable not found in .env file.")
        return None

    # Initialize your local pipeline package
    pipeline = TransitDataPipeline(db_url=DB_CONNECTION)
    
    logging.info("=== STARTING MULTI-TABLE DATA UPDATE ===")
    
    for table_name, api_endpoint in endpoints_to_sync.items():
        if not api_endpoint:
            #print(f"⚠ Skipping {table_name}: Endpoint URL is missing in .env config.")
            logging.info(f"Skipping {table_name}: Endpoint URL is missing in .env config.")
            continue
            
        pipeline.sync_endpoint(api_url=api_endpoint, target_table=table_name)
        
    logging.info("=== ALL DATABASE TABLES SUCCESSFULLY REFRESHED ===")
    return None

if __name__ == "__main__":
    main()