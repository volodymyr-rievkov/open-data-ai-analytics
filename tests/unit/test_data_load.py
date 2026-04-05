from unittest.mock import patch, MagicMock
from src.data_load.data_load import download_data 

def test_download_data_success(tmp_path):
    """Тест успішного завантаження даних."""
    fake_url = "https://fake-url.com/data.csv"
    temp_dir = tmp_path / "raw"
    save_path = temp_dir / "national_team.csv"
    fake_content = b"name;region;sport\nIvan;Kyiv;Judo"

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = fake_content
        mock_get.return_value = mock_response

        download_data(fake_url, str(save_path))

        mock_get.assert_called_once_with(fake_url)
        
        assert save_path.exists()
        
        with open(save_path, "rb") as f:
            assert f.read() == fake_content

def test_download_data_failure(tmp_path, capsys):
    """Тест випадку, коли сервер повернув помилку (наприклад, 404)."""
    fake_url = "https://fake-url.com/missing.csv"
    save_path = tmp_path / "should_not_exist.csv"

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        download_data(fake_url, str(save_path))

        assert not save_path.exists()
        
        captured = capsys.readouterr()
        assert "Error downloading data: 404" in captured.out
        