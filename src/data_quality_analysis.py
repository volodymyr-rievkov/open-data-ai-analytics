import pandas as pd
import os
from config import SAVE_PATH, PROCESSED_DATA_PATH

def data_quality_analysis():
    try:
        # Read data
        df = pd.read_csv(SAVE_PATH, sep=";") 
    except Exception as e:
        print(f"Error reading data: {e}")
        return

    # Define column types
    column_types = {
        'sport': 'string',
        'data': 'string',
        'type': 'string',
        'sex': 'string',
        'name': 'string',
        'rank': 'string',
        'fstName': 'string',
        'region': 'string',
        'discipline': 'string',
        'formerYearResultPlan': 'string',
        'formerYearResultFact': 'string',
        'currentYearResultPlan': 'string',
        'trainerName': 'string'
    }
    
    # Set column types
    for col, dtype in column_types.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)

    # Convert birthDate to datetime
    print("--- Converting birthDate to datetime ---")
    df['birthDate'] = pd.to_datetime(df["birthDate"], format='mixed', errors='coerce')
    if(df['birthDate'].isnull().any()):
        print("Note: 'birthDate' has invalid/missing dates (converted to NaT), filling with mode...")
        df['birthDate'] = df['birthDate'].fillna(df['birthDate'].mode()[0])

    # Check for missing values
    print("--- Missing values count per column ---")
    nan_info = df.isnull().sum()
    print(nan_info[nan_info > 0])

    # Fix missing values
    print("\nFilling missing values...")
    for col in df.columns:
        if df[col].isnull().any():
            count = df[col].isnull().sum()
            
            if df[col].dtype == 'string':
                df[col] = df[col].fillna("Не вказано")
                print(f"Fixed '{col}': filled {count} NaN values with 'Не вказано'")
            
            elif df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].fillna(pd.NaT)
                print(f"Note: '{col}' has {count} invalid/missing dates (converted to NaT)")
            
            else:
                df[col] = df[col].fillna(method='ffill')
                print(f"Fixed '{col}': filled {count} NaN values using ffill")

    # Final NaN check
    print("\nFinal NaN check:", df.isnull().sum().sum())

    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"\nProcessed data saved to: {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    data_quality_analysis()