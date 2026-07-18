# Script to update local NTD database from API endpoints.

# Import third-party dependencies
import logging
import os
from dotenv import load_workbook, load_dotenv

# Import local package
from ntd_data_extractor.extractor import TransitDataPipeline

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment and configuration parameters
load_dotenv()

DB_CONNECTION = os.environ.get("DB_CONNECTION")

endpoints_to_sync = {
    "ntd_annual_metrics":os.environ.get("API_ANNUAL_METRICS")
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