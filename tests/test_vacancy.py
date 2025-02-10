import pytest
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancy():
    return Vacancy(
        id="12345",
        name="Python Developer",
        salary={"from": 150000, "to": 200000, "currency": "RUR"},
        area="Москва",
        published_at="2025-02-10T10:00:00",
        url="https://hh.ru/vacancy/12345",
        employer={"name": "TechCorp", "url": "https://hh.ru/employer/99999"},
        experience="От 1 до 3 лет",
        schedule="Полный день",
    )


def test_create_vacancy(sample_vacancy):
    assert sample_vacancy.name == "Python Developer"
    assert sample_vacancy.salary["from"] == 150000
    assert sample_vacancy.area == "Москва"
    assert sample_vacancy.experience == "От 1 до 3 лет"


def test_from_api_response():
    api_data = {
        "id": "54321",
        "name": "Data Scientist",
        "salary": {"from": 180000, "to": 250000, "currency": "RUR"},
        "area": {"name": "Санкт-Петербург"},
        "published_at": "2025-02-09T12:00:00",
        "alternate_url": "https://hh.ru/vacancy/54321",
        "employer": {"name": "DataCorp", "alternate_url": "https://hh.ru/employer/88888"},
        "experience": {"name": "От 3 до 6 лет"},
        "schedule": {"name": "Удаленная работа"},
    }
    vacancy = Vacancy.from_api_response(api_data)

    assert vacancy.id == "54321"
    assert vacancy.name == "Data Scientist"
    assert vacancy.salary["from"] == 180000
    assert vacancy.area == "Санкт-Петербург"
    assert vacancy.experience == "От 3 до 6 лет"
    assert vacancy.schedule == "Удаленная работа"


def test_filter_by_salary():
    vacancies = [
        Vacancy("1", "Python Developer", {"from": 140000, "to": 180000, "currency": "RUR", "gross": True},
                "Москва", "2025-02-10", "http://example.com", {"name": "Company"}, "От 1 до 3 лет", "Полный день"),
        Vacancy("2", "Java Developer", {"from": None, "to": 150000, "currency": "RUR", "gross": True},
                "Москва", "2025-02-11", "http://example.com", {"name": "Company"}, "От 3 до 6 лет", "Полный день"),
        Vacancy("3", "Frontend Developer", {"from": 120000, "to": 130000, "currency": "RUR", "gross": True},
                "Москва", "2025-02-12", "http://example.com", {"name": "Company"}, "От 1 до 3 лет", "Полный день"),
        Vacancy("4", "Backend Developer", {},  # Вакансия без зарплаты
                "Москва", "2025-02-13", "http://example.com", {"name": "Company"}, "От 1 до 3 лет", "Полный день"),
    ]

    filtered = Vacancy.filter_by_salary(vacancies, 140000)
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"

    filtered = Vacancy.filter_by_salary(vacancies, 150000)
    assert len(filtered) == 2
    assert {vac.name for vac in filtered} == {"Python Developer", "Java Developer"}

    filtered = Vacancy.filter_by_salary(vacancies, 160000)
    assert len(filtered) == 1
    assert filtered[0].name == "Python Developer"

    filtered = Vacancy.filter_by_salary(vacancies, 200000)
    assert len(filtered) == 0



def test_filter_by_city(sample_vacancy):
    vacancies = [sample_vacancy]
    filtered = Vacancy.filter_by_city(vacancies, "Москва")
    assert len(filtered) == 1

    filtered = Vacancy.filter_by_city(vacancies, "Санкт-Петербург")
    assert len(filtered) == 0


def test_filter_by_experience(sample_vacancy):
    vacancies = [sample_vacancy]
    filtered = Vacancy.filter_by_experience(vacancies, "От 1 до 3 лет")
    assert len(filtered) == 1

    filtered = Vacancy.filter_by_experience(vacancies, "От 3 до 6 лет")
    assert len(filtered) == 0


def test_sort_by_salary():
    vacancies = [
        Vacancy("1", "Dev A", {"from": 100000, "to": 150000, "currency": "RUR"}, "Москва", "2025-02-10", "", {}, "",
                ""),
        Vacancy("2", "Dev B", {"from": 200000, "to": 250000, "currency": "RUR"}, "Москва", "2025-02-10", "", {}, "",
                ""),
    ]
    sorted_vacancies = Vacancy.sort_by_salary(vacancies)
    assert sorted_vacancies[0].name == "Dev B"
    assert sorted_vacancies[1].name == "Dev A"


def test_sort_by_date():
    vacancies = [
        Vacancy("1", "Dev A", {}, "Москва", "2025-02-09", "", {}, "", ""),
        Vacancy("2", "Dev B", {}, "Москва", "2025-02-10", "", {}, "", ""),
    ]
    sorted_vacancies = Vacancy.sort_by_date(vacancies)
    assert sorted_vacancies[0].name == "Dev B"
    assert sorted_vacancies[1].name == "Dev A"
