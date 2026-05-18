import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from src.utils import read_from_db, insert_into_db
from src.config import DB_URL, PROCESSED_DATA_TABLE, PLOTS_OUTPUT_PATH, PLOTS_TABLE

def create_visualizations(df):
    plots = []
    
    os.makedirs(PLOTS_OUTPUT_PATH, exist_ok=True)

    # Convert birthDate to datetime for age analysis
    df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
    df['age'] = 2023 - df['birthDate'].dt.year

    sns.set_theme(style="whitegrid")

    # 1. Visualization: Top 10 Regions (Bar Chart)
    plt.figure(figsize=(12, 6))
    region_counts = df['region'].value_counts().head(10)
    region_counts_df = region_counts.reset_index()
    sns.barplot(data=region_counts_df, x="count", y="region")
    plt.title("Top 10 Regions by Number of Athletes")
    plt.xlabel("Count")
    plt.ylabel("Region")
    plt.tight_layout()
    path = os.path.join(PLOTS_OUTPUT_PATH, "top_regions.png")
    plt.savefig(path)
    print(f"Saved to: {path}")
    plots.append({"plot_name": "top_regions", "file_path": path})

    # 2. Visualization: Age Distribution (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['age'].dropna(), bins=20, kde=True, color="skyblue")
    plt.title("Age Distribution of Athletes")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    path = os.path.join(PLOTS_OUTPUT_PATH, "age_distribution.png")
    plt.savefig(path)
    print(f"Saved to: {path}")
    plots.append({"plot_name": "age_distribution", "file_path": path})

    # 3. Visualization: Rank Distribution (Pie Chart)
    plt.figure(figsize=(8, 8))
    rank_data = df['rank'].value_counts().head(5)
    plt.pie(rank_data, labels=rank_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title("Distribution of Athlete Ranks (Top 5)")
    path = os.path.join(PLOTS_OUTPUT_PATH, "rank_distribution.png")
    plt.savefig(path)
    print(f"Saved to: {path}")
    plots.append({"plot_name": "rank_distribution", "file_path": path})

    return pd.DataFrame(plots)

if __name__ == "__main__":
    df = read_from_db(DB_URL, PROCESSED_DATA_TABLE)
    plots_df = create_visualizations(df)
    insert_into_db(plots_df, DB_URL, PLOTS_TABLE)