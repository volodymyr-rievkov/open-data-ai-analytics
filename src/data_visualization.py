import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from config import PROCESSED_DATA_PATH, PLOTS_OUTPUT_PATH

def create_visualizations():
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
        # Convert birthDate to datetime for age analysis
        df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
        df['age'] = 2023 - df['birthDate'].dt.year
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    sns.set_theme(style="whitegrid")

    # 1. Visualization: Top 10 Regions (Bar Chart)
    plt.figure(figsize=(12, 6))
    region_counts = df['region'].value_counts().head(10)
    sns.barplot(x=region_counts.values, y=region_counts.index, palette="viridis")
    plt.title("Top 10 Regions by Number of Athletes")
    plt.xlabel("Count")
    plt.ylabel("Region")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_OUTPUT_PATH, "top_regions.png"))
    print("Saved: top_regions.png")

    # 2. Visualization: Age Distribution (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['age'].dropna(), bins=20, kde=True, color="skyblue")
    plt.title("Age Distribution of Athletes")
    plt.xlabel("Age")
    plt.ylabel("Frequency")
    plt.savefig(os.path.join(PLOTS_OUTPUT_PATH, "age_distribution.png"))
    print("Saved: age_distribution.png")

    # 3. Visualization: Rank Distribution (Pie Chart)
    plt.figure(figsize=(8, 8))
    rank_data = df['rank'].value_counts().head(5)
    plt.pie(rank_data, labels=rank_data.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title("Distribution of Athlete Ranks (Top 5)")
    plt.savefig(os.path.join(PLOTS_OUTPUT_PATH, "rank_distribution.png"))
    print("Saved: rank_distribution.png")

if __name__ == "__main__":
    create_visualizations()