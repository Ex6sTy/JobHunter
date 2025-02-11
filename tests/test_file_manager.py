import json
from unittest.mock import patch, mock_open
from src.file_manager import JSONSaver
from src.vacancy import Vacancy


@patch("builtins.open", new_callable=mock_open, read_data='[]')
def test_load_vacancies(mock_file):
    vacancies = JSONSaver.load_vacancies()
    assert isinstance(vacancies, list)
    assert len(vacancies) == 0


@patch("builtins.open", new_callable=mock_open)
def test_save_vacancies(mock_file):
    vacancies = [Vacancy("123", "Python Dev", {}, "Москва", "2025-02-10", "https://hh.ru/vacancy/123", {}, "1-3 года",
                         "Полный день")]
    JSONSaver.save_vacancies(vacancies)

    mock_file.assert_called_once_with(JSONSaver.FILE_PATH, "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called()


@patch("builtins.open", new_callable=mock_open, read_data=json.dumps([{"id": "123", "name": "Python Dev"}]))
def test_delete_vacancy_by_user_input(mock_file):
    with patch("builtins.input", return_value="123"):
        JSONSaver.delete_vacancy_by_user_input()

    handle = mock_file()
    handle.write.assert_called()
