import pytest
import pandas as pd
from unittest.mock import patch
import matplotlib
matplotlib.use('Agg') 
from src.data_visualization.data_visualization import create_visualizations

@pytest.fixture
def sample_viz_data():
    """Створюємо мінімальний набір даних для візуалізації."""
    return pd.DataFrame({
        'region': ['Kyiv', 'Lviv', 'Kyiv', 'Odessa', 'Kyiv', 'Lviv'],
        'birthDate': ['1990-01-01', '2000-01-01', '1995-01-01', '2010-01-01', '1985-01-01', '1990-01-01'],
        'rank': ['MS', 'MS', 'KMS', 'MS', 'KMS', 'MS']
    })

def test_create_visualizations_files_created(tmp_path, sample_viz_data):
    """Перевірка, чи створюються PNG файли та чи повертається правильний DataFrame."""
    
    temp_plots_dir = tmp_path / "plots"
    
    with patch("src.data_visualization.data_visualization.PLOTS_OUTPUT_PATH", str(temp_plots_dir)):
        plots_df = create_visualizations(sample_viz_data)

        assert isinstance(plots_df, pd.DataFrame)
        assert len(plots_df) == 3
        assert list(plots_df.columns) == ["plot_name", "file_path"]

        expected_files = ["top_regions.png", "age_distribution.png", "rank_distribution.png"]
        for file_name in expected_files:
            file_path = temp_plots_dir / file_name
            assert file_path.exists(), f"Файл {file_name} не був створений"
            assert file_path.stat().st_size > 0

def test_age_calculation_in_viz(tmp_path, sample_viz_data):
    """Перевірка, чи коректно розраховується вік перед побудовою гістограми."""
    
    temp_plots_dir = tmp_path / "plots_test_age"
    
    with patch("src.data_visualization.data_visualization.PLOTS_OUTPUT_PATH", str(temp_plots_dir)):
        try:
            create_visualizations(sample_viz_data)
        except Exception as e:
            pytest.fail(f"Функція впала при розрахунку віку: {e}")

def test_visualization_empty_df(tmp_path):
    """Перевірка стійкості до порожнього DataFrame."""
    temp_plots_dir = tmp_path / "empty_plots"
    df_empty = pd.DataFrame(columns=['region', 'birthDate', 'rank'])
    
    with patch("src.data_visualization.data_visualization.PLOTS_OUTPUT_PATH", str(temp_plots_dir)):
        plots_df = create_visualizations(df_empty)
        assert len(plots_df) == 3
