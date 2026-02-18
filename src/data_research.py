import pandas as pd
import os

# Using the processed data from the previous stage
PROCESSED_DATA_PATH = os.path.join("data", "processed", "national_team_2023.csv")

def data_research():
    """
    Performs basic statistical analysis and hypothesis testing on processed sports data.
    """
    try:
        # Load cleaned dataset
        df = pd.read_csv(PROCESSED_DATA_PATH)
        print(f"--- Data research started. Dataset size: {len(df)} rows ---")
    except Exception as e:
        print(f"Error during data loading: {e}")
        return

    # HYPOTHESIS 1: Regional and Organizational Leadership
    print("\n[H1] Top 5 Regions by Athlete Count:")
    print(df['region'].value_counts().head(5))
    
    print("\n[H1] Top 5 Sports Societies (FST):")
    print(df[df['fstName'] != "Не вказано"]['fstName'].value_counts().head(5))

    # HYPOTHESIS 2: Planning Efficiency
    # Basic model: Comparing planned vs. actual results to check prediction accuracy
    valid_mask = (df['formerYearResultPlan'] != "Не вказано") & \
                 (df['formerYearResultFact'] != "Не вказано")
    
    planning_accuracy = (df[valid_mask]['formerYearResultPlan'] == 
                         df[valid_mask]['formerYearResultFact']).mean() * 100
    print(f"\n[H2] Planning accuracy (Match between Plan and Fact): {planning_accuracy:.2f}%")

    # HYPOTHESIS 3: Age and Qualification Profiles
    # Age calculation based on birthDate
    df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
    reference_year = 2023
    df['age'] = reference_year - df['birthDate'].dt.year
    
    print(f"\n[H3] Average athlete age: {df['age'].mean():.1f} years")
    print("\n[H3] Qualification rank distribution (Top 5):")
    print(df['rank'].value_counts().head(5))

    # PRIMITIVE MODEL: Cross-tabulation of Rank vs. Sport
    # Analyzing how sports degrees are distributed within the most popular sports
    top_sports = df['sport'].value_counts().head(3).index
    model_data = df[df['sport'].isin(top_sports)]
    
    rank_model = pd.crosstab(model_data['sport'], model_data['rank'], normalize='index') * 100
    print("\n[Model] Probability matrix: Rank distribution by Sport (%)")
    print(rank_model.round(1))

    print("\n--- Research completed successfully ---")

if __name__ == "__main__":
    data_research()