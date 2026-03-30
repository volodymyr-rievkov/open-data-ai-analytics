import pandas as pd

from src.config import RAW_DATA_TABLE, DB_URL, PROCESSED_DATA_PATH, PROCESSED_DATA_TABLE, QUALITY_REPORT_PATH
from src.utils import read_from_db, insert_into_db, read_csv, save_csv, save_json

def data_quality_analysis(df):
    # Convert birthDate to datetime
    print("--- Converting birthDate to datetime ---")
    df['birthDate'] = pd.to_datetime(df["birthDate"], format='mixed', errors='coerce')
    
    quality_report = {
        "initial_rows": len(df),
        "missing_values_before": df.isnull().sum().to_dict(),
        "fixed_columns": {}
    }

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

    # Check for missing values
    print("--- Missing values count per column ---")
    print(quality_report["missing_values_before"])

    if(df['birthDate'].isnull().any()):
        count = int(df['birthDate'].isnull().sum())
        mode_val = df['birthDate'].mode()[0]
        df['birthDate'] = df['birthDate'].fillna(mode_val)        
        quality_report["fixed_columns"]["birthDate"] = f"Filled {count} NaT with mode"
        print(quality_report["fixed_columns"]["birthDate"])

    # Fix missing values
    print("\nFilling missing values...")
    for col in df.columns:
        if df[col].isnull().any():
            count = int(df[col].isnull().sum())
            
            if df[col].dtype == 'string':
                df[col] = df[col].fillna("Не вказано")
                quality_report["fixed_columns"][col] = f"Filled {count} NaN with 'Не вказано'"
            
            elif df[col].dtype == 'datetime64[ns]':
                df[col] = df[col].fillna(pd.NaT)
                quality_report["fixed_columns"][col] = f"Converted {count} invalid dates to NaT"
            
            else:
                df[col] = df[col].ffill()
                quality_report["fixed_columns"][col] = f"Filled {count} NaN using ffill"

            print(quality_report["fixed_columns"][col])

    quality_report["final_nan_count"] = df.isnull().sum().to_dict()
    print("\nFinal NaN check:", quality_report["final_nan_count"])
    
    return df, quality_report
    

if __name__ == "__main__":
    df = read_from_db(DB_URL, RAW_DATA_TABLE)
    df, quality_report = data_quality_analysis(df)
    save_csv(df, PROCESSED_DATA_PATH)
    save_json(quality_report, QUALITY_REPORT_PATH)

    df = read_csv(PROCESSED_DATA_PATH, sep=",")
    insert_into_db(df, DB_URL, table_name=PROCESSED_DATA_TABLE)