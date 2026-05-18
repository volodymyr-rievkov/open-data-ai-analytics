import pytest
import pandas as pd
import json
from src.utils import read_csv, save_csv, insert_into_db, read_from_db, save_json

@pytest.fixture
def sample_df():
    """Фікстура для створення тестового DataFrame."""
    return pd.DataFrame({
        "id": [1, 2],
        "name": ["Test1", "Test2"],
        "value": [10.5, 20.0]
    })

def test_save_and_read_csv(tmp_path, sample_df):
    """Перевірка збереження та наступного читання CSV."""
    d = tmp_path / "data"
    d.mkdir()
    file_path = d / "test.csv"
    
    save_csv(sample_df, str(file_path))
    
    df_read = read_csv(str(file_path), sep=",")
    
    assert len(df_read) == 2
    assert list(df_read.columns) == ["id", "name", "value"]

def test_save_json(tmp_path):
    """Перевірка збереження словника в JSON."""
    report = {"status": "ok", "count": 100}
    file_path = tmp_path / "report.json"
    
    save_json(report, str(file_path))
    
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == report

def test_db_operations(tmp_path, sample_df):
    """Тест 'туди-сюди': запис в базу і читання з неї."""
    db_file = tmp_path / "test_project.db"
    db_url = f"sqlite:///{db_file}"
    table_name = "test_table"
    
    insert_into_db(sample_df, db_url, table_name)
    
    df_from_db = read_from_db(db_url, table_name)
    
    assert len(df_from_db) == 2
    assert "name" in df_from_db.columns
    pd.testing.assert_frame_equal(sample_df, df_from_db)

def test_read_csv_file_not_found():
    """Перевірка, чи функція кидає Exception, якщо файлу немає."""
    with pytest.raises(Exception):
        read_csv("non_existent_file.csv")

def test_read_from_db_wrong_table():
    """Перевірка помилки при читанні неіснуючої таблиці."""
    db_url = "sqlite:///:memory:" 
    with pytest.raises(Exception):
        read_from_db(db_url, "ghost_table")