import requests
import os
from src.config import DATA_URL, SAVE_PATH, DB_URL, RAW_DATA_TABLE
from src.utils import read_csv, insert_into_db

def download_data(data_url, save_path):    
    print(f"Loading data from {data_url}...")
    response = requests.get(data_url)
    
    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Data successfully downloaded to {save_path}")
    else:
        print(f"Error downloading data: {response.status_code}")


if __name__ == "__main__":
    download_data(DATA_URL, SAVE_PATH)
    df = read_csv(SAVE_PATH)
    insert_into_db(df, DB_URL, table_name=RAW_DATA_TABLE)
