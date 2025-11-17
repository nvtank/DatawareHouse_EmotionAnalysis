import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()

def get_db_url():
    """Create database connection URL from .env file"""
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    db = os.getenv('POSTGRES_DB')
    
    if not all([user, password, host, port, db]):
        print("Error: Some environment variables (.env) are missing.")
        sys.exit(1)
        
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"

def load_data_to_db():
    """Main function: Read CSV and Load into PostgreSQL"""
    
    db_url = get_db_url()
    file_path = 'data/affectnet_processed_results.csv'
    table_name = 'stg_affectnet_raw' # Staging table name (raw)
    
    try:
        # 1. Extract (Read CSV file)
        print(f"Reading data from {file_path}...")
        df = pd.read_csv(file_path)
        
        # 2. Minor processing: Ensure timestamp is datetime type
        df['capture_timestamp'] = pd.to_datetime(df['capture_timestamp'])
        print(f"Read {len(df)} rows of data.")

        # 3. Load (Load into PostgreSQL)
        print(f"Connecting to database {os.getenv('POSTGRES_DB')}...")
        engine = create_engine(db_url)
        
        print(f"Loading data into table '{table_name}' (Schema: public)...")
        # if_exists='replace': Drop old table if exists and create new table
        df.to_sql(table_name, engine, if_exists='replace', index=False, schema='public')
        
        print("\n--- SUCCESS! ---")
        print(f"Data has been successfully loaded into table '{table_name}'.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{file_path}'.")
    except Exception as e:
        print(f"Error during E/L process: {e}")

if __name__ == "__main__":
    load_data_to_db()