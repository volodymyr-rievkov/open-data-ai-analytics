import pandas as pd
import requests
import os

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
    SAVE_PATH = "data/raw/national_team_2023.csv"
    DATA_URL = "https://data.gov.ua/dataset/abd6229a-4cd8-4cc2-b6ca-793978e42b10/resource/a2465815-7d53-4a22-863b-493a0aab1d10/download/2023-national-team.csv"
    
    download_data(DATA_URL, SAVE_PATH)
    
    df = pd.read_csv(SAVE_PATH, sep=";") 
    print(df.head())