# Core engine to extract data from endpoints

# Import dependencies
import pandas as pd
import requests
from sqlalchemy import create_engine
import time
import logging

# Set up clean terminal logging instead of basic print statements
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransitDataPipeline:
    """Manages connections and streams data from Socrata APIs into PostgreSQL."""
    
    def __init__(self, db_url: str):
        """Initialize the pipeline with a target database connection string."""
        self.db_url = db_url
        self.engine = create_engine(db_url)
        
    def sync_endpoint(self, api_url: str, target_table: str, page_size: int = 50000):
        """Fetch all pages from a Socrata API endpoint and overwrite a Postgres table."""
        offset = 0
        all_chunks = []
        logging.info(f"Starting sync for table '{target_table}' from endpoint: {api_url}")
        
        while True:
            params = {
                "$limit": page_size,
                "$offset": offset,
                "$order": ":id"
            }
            
            try:
                response = requests.get(api_url, params=params)
                response.raise_for_status() # Automatically catch bad HTTP statuses
                data = response.json()
                
                if not data:
                    logging.info(f"Reached end of data stream for '{target_table}'.")
                    break
                    
                chunk_df = pd.DataFrame(data)
                all_chunks.append(chunk_df)
                
                logging.info(f"[{target_table}] Fetched rows {offset} to {offset + len(data)}")
                offset += page_size
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"Failed processing chunk at offset {offset} for table '{target_table}': {e}")
                return # Exit this specific sync execution if it breaks
                
        if all_chunks:
            # Combine chunks and format column names for SQL safety
            master_df = pd.concat(all_chunks, ignore_index=True)
            master_df.columns = [c.lower().replace(' ', '_') for c in master_df.columns]
            
            logging.info(f"Pouring {len(master_df)} rows into Postgres table '{target_table}'...")
            
            # Write to SQL
            master_df.to_sql(target_table, con=self.engine, if_exists='replace', index=False)
            logging.info(f"Success! Table '{target_table}' is fully updated.")
        else:
            logging.warning(f"No data recovered for table '{target_table}'.")