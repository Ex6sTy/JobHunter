from src.api_connector import HeadHunterAPI

def test_get_vacancies():
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python")
    assert isinstance(vacancies, list), "Должен вернуть список вакансий"
    assert len(vacancies) > 0, "Должен вернуть как минимум одну вакансию"