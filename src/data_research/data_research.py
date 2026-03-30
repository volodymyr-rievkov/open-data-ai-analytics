import pandas as pd
from src.config import DB_URL, PROCESSED_DATA_TABLE, RESEARCH_REPORT_PATH
from src.utils import read_from_db, save_json

def data_research(df):
    """
    Performs basic statistical analysis and hypothesis testing on processed sports data.
    """
    results = {}
    # HYPOTHESIS 1: Regional and Organizational Leadership
    print("\n[H1] Top 5 Regions by Athlete Count:")
    top_regions = df['region'].value_counts().head(5)
    print(top_regions)
    results['top_regions'] = top_regions.to_dict()

    print("\n[H1] Top 5 Sports Societies (FST):")
    top_fsts = df[df['fstName'] != "Не вказано"]['fstName'].value_counts().head(5)
    print(top_fsts)
    results['top_fsts'] = top_fsts.to_dict()

    # HYPOTHESIS 2: Planning Efficiency
    # Basic model: Comparing planned vs. actual results to check prediction accuracy
    valid_mask = (df['formerYearResultPlan'] != "Не вказано") & \
                 (df['formerYearResultFact'] != "Не вказано")
    
    planning_accuracy = (df[valid_mask]['formerYearResultPlan'] == 
                         df[valid_mask]['formerYearResultFact']).mean() * 100
    print(f"\n[H2] Planning accuracy (Match between Plan and Fact): {planning_accuracy:.2f}%")
    results['planning_accuracy_pct'] = round(planning_accuracy, 2)

    # HYPOTHESIS 3: Age and Qualification Profiles
    # Age calculation based on birthDate
    df['birthDate'] = pd.to_datetime(df['birthDate'], errors='coerce')
    reference_year = 2023
    df['age'] = reference_year - df['birthDate'].dt.year
    
    avg_age = df['age'].mean()
    print(f"\n[H3] Average athlete age: {avg_age:.1f} years")
    results['avg_age'] = round(avg_age, 1)

    print("\n[H3] Qualification rank distribution (Top 5):")
    top_ranks = df['rank'].value_counts().head(5)
    print(top_ranks)
    results['rank_distribution'] = top_ranks.to_dict()

    # PRIMITIVE MODEL: Cross-tabulation of Rank vs. Sport
    # Analyzing how sports degrees are distributed within the most popular sports
    top_sports = df['sport'].value_counts().head(3).index
    model_data = df[df['sport'].isin(top_sports)]
    
    rank_model = pd.crosstab(model_data['sport'], model_data['rank'], normalize='index') * 100
    print("\n[Model] Probability matrix: Rank distribution by Sport (%)")
    print(rank_model.round(1))
    results['rank_probability_matrix'] = rank_model.round(1).to_dict()

    print("\n--- Research completed successfully ---")
    return results


if __name__ == "__main__":
    df = read_from_db(DB_URL, PROCESSED_DATA_TABLE)
    reports = data_research(df)
    save_json(reports, RESEARCH_REPORT_PATH)