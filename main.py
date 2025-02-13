import logging
from src.api_connector import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_manager import JSONSaver

def main():
    search_text = input("Введите название вакансии: ").strip()
    if not search_text:
        print("Название вакансии не может быть пустым!")
        return

    api = HeadHunterAPI()

    if JSONSaver.has_saved_vacancies():
        use_saved = input("Использовать сохраненные вакансии? (да/нет): ").strip().lower()
        vacancies_data = JSONSaver.load_vacancies() if use_saved == "да" else api.get_vacancies(search_text)
    else:
        vacancies_data = api.get_vacancies(search_text)

    # Преобразуем словари в объекты Vacancy
    vacancies = [Vacancy.from_api_response(data) for data in vacancies_data]

    logging.info(f"Получено {len(vacancies)} вакансий")

    if not vacancies:
        print("Нет данных о вакансиях.")
        return

    filter_choice = input("Хотите фильтровать вакансии? (да/нет): ").strip().lower()
    if filter_choice == "да":
        min_salary = input("Введите минимальную зарплату (оставьте пустым, чтобы пропустить): ").strip()
        if min_salary.isdigit():
            vacancies = Vacancy.filter_by_salary(vacancies, min_salary)

        city = input("Введите город (оставьте пустым, чтобы пропустить): ").strip()
        if city:
            vacancies = Vacancy.filter_by_city(vacancies, city)

        experience = input("Введите требуемый опыт (Нет опыта, От 1 до 3 лет, От 3 до 6 лет, От 6 лет): ").strip()
        if experience:
            vacancies = Vacancy.filter_by_experience(vacancies, experience)

        sort_option = input("Сортировать вакансии по (зарплата/дата)? ").strip().lower()
        if sort_option == "зарплата":
            if isinstance(vacancies, list):
                vacancies = Vacancy.sort_by_salary(vacancies)
            else:
                logging.error(f"Ошибка: переменная vacancies не является списком. Текущее значение: {vacancies}")
                return
        elif sort_option == "дата":
            if isinstance(vacancies, list):
                vacancies = Vacancy.sort_by_date(vacancies)
            else:
                logging.error(f"Ошибка: переменная vacancies не является списком. Текущее значение: {vacancies}")
                return

    if not vacancies:
        print("После фильтрации не осталось ни одной вакансии.")
        return

    JSONSaver.save_vacancies(vacancies)
    print(f"Сохранено {len(vacancies)} вакансий в {JSONSaver.FILE_PATH}")

    for vac in vacancies[:10]:
        print(f"{vac.name} - {vac.get_salary()} руб. - {vac.area} ({vac.url})")

    delete_choice = input("Хотите удалить вакансию? (да/нет): ").strip().lower()
    if delete_choice == "да":
        JSONSaver.delete_vacancy_by_user_input()

if __name__ == "__main__":
    main()
