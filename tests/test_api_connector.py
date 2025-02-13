from unittest.mock import patch, mock_open
from src.api_connector import HeadHunterAPI


@patch("requests.get")
def test_get_vacancies(mock_get):
    mock_response = {
        "items": [
            {
                "id": "123",
                "name": "Python Developer",
                "salary": {"from": 150000},
                "area": {"name": "Москва"},
                "published_at": "2025-02-10T12:00:00",
                "alternate_url": "https://hh.ru/vacancy/123"
            }
        ]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200  # Добавляем статус 200

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")

    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Python Developer"
