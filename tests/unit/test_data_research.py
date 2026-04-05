import pytest
import pandas as pd
from src.data_research.data_research import data_research

@pytest.fixture
def sample_research_data():
    """Створюємо контрольний набір даних для перевірки статистики."""
    return pd.DataFrame({
        'region': ['Kyiv', 'Kyiv', 'Lviv', 'Odessa', 'Kyiv', 'Lviv'],
        'fstName': ['Dynamo', 'Dynamo', 'Spartak', 'Не вказано', 'Dynamo', 'Spartak'],
        'formerYearResultPlan': ['Win', 'Win', 'Loss', 'Win', 'Не вказано', 'Win'],
        'formerYearResultFact': ['Win', 'Loss', 'Loss', 'Win', 'Win', 'Win'],
        'birthDate': ['1990-01-01', '2000-01-01', '1995-01-01', '2010-01-01', '1985-01-01', '1990-01-01'],
        'rank': ['MS', 'MS', 'KMS', 'MS', 'KMS', 'MS'],
        'sport': ['Judo', 'Judo', 'Boxing', 'Judo', 'Boxing', 'Boxing']
    })

def test_data_research_leadership(sample_research_data):
    """Тест Гіпотези 1: Регіони та Спортивні товариства."""
    results = data_research(sample_research_data)
    
    assert results['top_regions']['Kyiv'] == 3
    
    assert 'Не вказано' not in results['top_fsts']
    assert results['top_fsts']['Dynamo'] == 3

def test_data_research_planning_accuracy(sample_research_data):
    """Тест Гіпотези 2: Ефективність планування."""
    results = data_research(sample_research_data)
    
    assert results['planning_accuracy_pct'] == 80.0

def test_data_research_age(sample_research_data):
    """Тест Гіпотези 3: Середній вік."""
    results = data_research(sample_research_data)
    
    assert results['avg_age'] == 28.0

def test_data_research_model_matrix(sample_research_data):
    """Тест моделі: крос-табуляція."""
    results = data_research(sample_research_data)
    
    assert 'rank_probability_matrix' in results
    assert isinstance(results['rank_probability_matrix'], dict)

    assert results['rank_probability_matrix']['MS']['Judo'] == 100.0

def test_data_research_empty_handling():
    """Тест на стійкість до порожніх даних."""
    empty_df = pd.DataFrame(columns=['region', 'fstName', 'formerYearResultPlan', 
                                     'formerYearResultFact', 'birthDate', 'rank', 'sport'])
    results = data_research(empty_df)
    assert isinstance(results, dict)
    