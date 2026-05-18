import pandas as pd
import numpy as np
from src.data_quality_analysis.data_quality_analysis import data_quality_analysis

def test_data_quality_logic():
    """Перевірка основної логіки очищення даних."""
    data = {
        "birthDate": ["2000-01-01", "02/05/1995", "invalid-date", None],
        "sport": ["Judo", None, "Boxing", "Judo"],
        "name": ["Ivan", "Petro", None, "Oleg"],
        "some_numeric": [10, np.nan, 30, np.nan]
    }
    df = pd.DataFrame(data)

    df_cleaned, report = data_quality_analysis(df.copy())

    assert not df_cleaned["birthDate"].isnull().any()
    assert pd.api.types.is_datetime64_any_dtype(df_cleaned["birthDate"])

    assert df_cleaned["sport"].iloc[1] == "Не вказано"
    assert df_cleaned["name"].iloc[2] == "Не вказано"

    assert df_cleaned["some_numeric"].iloc[1] == 10
    assert df_cleaned["some_numeric"].iloc[3] == 30

    assert report["initial_rows"] == 4
    assert "birthDate" in report["fixed_columns"]
    assert report["final_nan_count"]["sport"] == 0

def test_data_quality_empty_df():
    """Перевірка роботи з порожнім DataFrame."""
    df_empty = pd.DataFrame(columns=["birthDate", "sport"])
    df_cleaned, report = data_quality_analysis(df_empty)
    
    assert len(df_cleaned) == 0
    assert report["initial_rows"] == 0
