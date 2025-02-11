import logging
from src.api_connector import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_manager import JSONSaver


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def filter_vacancies(vacancies, search_text):
    filtered = []
    for vacancy in vacancies:
        name = vacancy.name.lower() if isinstance(vacancy, Vacancy) else vacancy["name"].lower()
        if search_text.lower() in name:
            filtered.append(vacancy)
    return filtered


def main():
    search_text = input("Введите название вакансии: ").strip()
    if not search_text:
        print("Название вакансии не может быть пустым!")
        return

    if JSONSaver.has_saved_vacancies():  # Проверяем, есть ли сохраненные вакансии
        use_saved = input("Использовать сохраненные вакансии? (да/нет): ").strip().lower()
        vacancies = JSONSaver.load_vacancies() if use_saved == "да" else HeadHunterAPI().get_vacancies(search_text)
    else:
        vacancies = HeadHunterAPI().get_vacancies(search_text)

    vacancies = filter_vacancies(vacancies, search_text)
    logging.info(f"После фильтрации осталось {len(vacancies)} вакансий")

    if not vacancies:
        print("Нет данных о вакансиях по вашему запросу.")
        return

    min_salary = int(input("Введите минимальную зарплату: "))
    vacancies = Vacancy.filter_by_salary(vacancies, min_salary)

    city = input("Введите город (оставьте пустым, чтобы пропустить): ").strip()
    if city:
        vacancies = Vacancy.filter_by_city(vacancies, city)

    experience = input("Введите требуемый опыт (Нет опыта, От 1 до 3 лет, От 3 до 6 лет, От 6 лет): ").strip()
    if experience:
        vacancies = Vacancy.filter_by_experience(vacancies, experience)

    if not vacancies:
        print("После фильтрации вакансий не найдено.")
        return

    sort_option = input("Сортировать вакансии по (зарплата/дата)? ").strip().lower()
    if sort_option == "зарплата":
        vacancies = Vacancy.sort_by_salary(vacancies)
    elif sort_option == "дата":
        vacancies = Vacancy.sort_by_date(vacancies)

    JSONSaver.save_vacancies(vacancies)
    logging.info(f"Сохранено {len(vacancies)} вакансий в {JSONSaver.FILE_PATH}")

    for vac in vacancies[:10]:
        print(f"{vac.name} - {vac.get_salary()} руб. - {vac.area} ({vac.url})")

    delete_choice = input("Хотите удалить вакансию? (да/нет): ").strip().lower()
    if delete_choice == "да":
        JSONSaver.delete_vacancy_by_user_input()


if __name__ == "__main__":
    main()
