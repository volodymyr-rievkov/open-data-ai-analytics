import pandas as pd
import os
import json
from sqlalchemy import create_engine

def read_csv(csv_path, sep=";"):
    try:
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path, sep=sep) 
    except Exception as e:
        print(f"Error reading data: {e}")
        raise
    else:
        print(f"Data successfully read from {csv_path} ({len(df)} rows)")
        return df
    
def save_csv(df, save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        print(f"Saving processed data to {save_path}...")
        df.to_csv(save_path, index=False)
    except Exception as e:
        print(f"Error saving data: {e} ---")
        raise
    else:
        print(f"\nProcessed data saved to: {save_path}")

def insert_into_db(df, db_url, table_name):
    try:
        print(f"Connecting to database at {db_url}...")
        engine = create_engine(db_url)
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Database insertion failed: {e}")
        raise
    else:
        print(f"Data successfully inserted into table '{table_name}' ({len(df)} rows)")

def read_from_db(db_url, table_name):
    try:
        print(f"Reading table '{table_name}' from {db_url}...")
        engine = create_engine(db_url)
        df = pd.read_sql_table(table_name, con=engine)
    except Exception as e:
        print(f"Failed to read from database: {e} ---")
        raise
    else:
        print(f"Successfully read {len(df)} rows.")
        return df
    
def save_json(dict, save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        print(f"Saving processed data to {save_path}...")
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving data: {e} ---")
        raise
    else:
        print(f"\nJSON data saved to: {save_path}")
