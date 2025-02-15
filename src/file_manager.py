import json
from src.vacancy import Vacancy
from src.api_connector import HeadHunterAPI
import os


class JSONSaver:
    FILE_PATH = "vacancies.json"

    @staticmethod
    def save_vacancies(vacancies: list[Vacancy]):
        """ Сохрнаяет список вакансий в JSON-файл """
        with open(JSONSaver.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([vac.to_dict() if isinstance(vac, Vacancy) else vac for vac in vacancies],
                      f, ensure_ascii=False, indent=4)

    @staticmethod
    def has_saved_vacancies():
        """ Проверяет, есть ли сохраненные вакансии. """
        return os.path.exists(JSONSaver.FILE_PATH) and os.path.getsize(JSONSaver.FILE_PATH) > 0

    @staticmethod
    def load_vacancies() -> list[Vacancy]:
        """ Загружает вакансии из JSON-файла """
        try:
            with open(JSONSaver.FILE_PATH, "r", encoding="utf-8") as f:
                vacancies_data = json.load(f)
            return [Vacancy.from_api_response(data) for data in vacancies_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def delete_vacancy(vacancy_id: str):
        """Удаляет вакансию по её ID из JSON-файла."""
        vacancies = JSONSaver.load_vacancies()
        new_vacancies = [vac for vac in vacancies if vac.id != vacancy_id]

        if len(new_vacancies) == len(vacancies):
            print(f"Вакансия с ID {vacancy_id} не найдена.")
        else:
            JSONSaver.save_vacancies(new_vacancies)
            print(f"Вакансия {vacancy_id} удалена.")

    @staticmethod
    def delete_vacancy_by_user_input():
        """Позволяет пользователю удалить вакансию через консоль."""
        vacancies = JSONSaver.load_vacancies()
        if not vacancies:
            print("Нет сохраненных вакансий.")
            return

        print("Сохранённые вакансии:")
        for vac in vacancies[:10]:  # Показываем до 10 вакансий
            print(f"{vac.id} - {vac.name}")

        vacancy_id = input("Введите ID вакансии, которую хотите удалить: ")
        JSONSaver.delete_vacancy(vacancy_id)

    @staticmethod
    def load_or_fetch_vacancies(search_text):
        """ Загружает вакансии из файла или делает запрос к API """
        use_saved = input("Использовать сохраненные вакансии? (да/нет): ").strip().lower()

        if use_saved == "да":
            print("DEBUG: Загружаем вакансии из кеша...")
            return JSONSaver.load_vacancies()

        print(f"DEBUG: Запрашиваем вакансии для '{search_text}' из API...")
        vacancies = HeadHunterAPI().get_vacancies(search_text)

        JSONSaver.save_vacancies(vacancies)
        return vacancies
