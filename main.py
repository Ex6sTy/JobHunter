from src.api_connector import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_manager import JSONSaver

def filter_vacancies(vacancies, search_text):
    return [vacancy for vacancy in vacancies
            if search_text.lower() in (vacancy.name.lower() if isinstance(vacancy, Vacancy) else vacancy["name"].lower())]

def main():
    search_text = input("Введите название вакансии: ").strip()

    if not search_text:
        print("Название вакансии не может быть пустым!")
        return

    api = HeadHunterAPI()  # ✅ Создаем объект API-клиента

    use_saved = input("Использовать сохраненные вакансии? (да/нет): ").strip().lower()
    if use_saved == "да":
        vacancies = JSONSaver.load_vacancies()
    else:
        vacancies = api.get_vacancies(search_text)  # ✅ Теперь api определен

    vacancies = filter_vacancies(vacancies, search_text)
    print(f"DEBUG: После фильтрации осталось {len(vacancies)} вакансий")

    if not vacancies:
        print("Нет данных о вакансиях.")
        return

    # Фильтр по зарплате
    try:
        min_salary = int(input("Введите минимальную зарплату: "))
        vacancies = Vacancy.filter_by_salary(vacancies, min_salary)
    except ValueError:
        print("Некорректный ввод зарплаты. Фильтр по зарплате пропущен.")

    # Фильтр по городу
    city = input("Введите город (оставьте пустым, чтобы пропустить): ").strip()
    if city:
        vacancies = Vacancy.filter_by_city(vacancies, city)

    # Фильтр по опыту
    experience = input("Введите требуемый опыт (Нет опыта, От 1 до 3 лет, От 3 до 6 лет, От 6 лет): ").strip()
    if experience:
        vacancies = Vacancy.filter_by_experience(vacancies, experience)

    # Выбор сортировки
    sort_option = input("Сортировать вакансии по (зарплата/дата)? ").strip().lower()
    if sort_option == "зарплата":
        vacancies = Vacancy.sort_by_salary(vacancies)
    elif sort_option == "дата":
        vacancies = Vacancy.sort_by_date(vacancies)

    # Сохранение вакансий в JSON
    JSONSaver.save_vacancies(vacancies)
    print(f"Сохранено {len(vacancies)} вакансий в {JSONSaver.FILE_PATH}")

    for vac in vacancies[:10]:  # Выводим первые 10 вакансий
        print(f"{vac.name} - {vac.get_salary()} руб. - {vac.area} ({vac.url})")

    # Пользователь может удалить вакансию
    delete_choice = input("Хотите удалить вакансию? (да/нет): ").strip().lower()
    if delete_choice == "да":
        JSONSaver.delete_vacancy_by_user_input()

if __name__ == "__main__":
    main()
