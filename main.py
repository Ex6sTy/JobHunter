from src.api_connector import HeadHunterAPI
from src.vacancy import Vacancy

def main():
    api = HeadHunterAPI()
    vacancies_data = api.get_vacancies("HR")  # Загружаем вакансии

    if not vacancies_data:  # Проверяем, не пуст ли список
        print("Нет данных о вакансиях.")
        return

    # Проверяем, что `vacancies_data` содержит словари
    if not isinstance(vacancies_data[0], dict):
        print("Ошибка: данные о вакансиях имеют неверный формат.")
        return

    vacancies = [Vacancy.from_api_response(v) for v in vacancies_data]  # Создаём объекты Vacancy

    min_salary = int(input("Введите минимальную зарплату: "))
    vacancies = Vacancy.filter_by_salary(vacancies, min_salary)

    for vac in vacancies:
        print(f"{vac.name} - {vac.get_salary()} руб. - {vac.area} ({vac.url})")

if __name__ == "__main__":
    main()



