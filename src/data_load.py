import pandas as pd
import requests
import os

from config import DATA_URL, SAVE_PATH

def download_data(url, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    print(f"Loading data from {url}...")
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Data saved to: {save_path}")
    else:
        print(f"Error downloading data: {response.status_code}")

if __name__ == "__main__":
    download_data(DATA_URL, SAVE_PATH)
    
    df = pd.read_csv(SAVE_PATH, sep=";") 
    print(df.head())