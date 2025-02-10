from datetime import datetime


class Vacancy:
    def __init__(self, id: str, name: str, salary: dict, area: str, published_at: str, url: str, employer: dict, experience: str, schedule: str):
        self.id = id
        self.name = name
        self.salary = salary
        self.area = area
        self.published_at = published_at
        self.url = url
        self.employer = employer
        self.experience = experience
        self.schedule = schedule

    @staticmethod
    def from_api_response(data):
        return Vacancy(
            id=data.get("id", ""),
            name=data.get("name", "Не указано"),
            salary=data.get("salary", {}),
            area=data.get("area", {}).get("name", "Не указан") if isinstance(data.get("area"), dict) else data.get("area", "Не указан"),
            published_at=data.get("published_at", ""),
            url=data.get("url", ""),
            employer=data.get("employer", {}).get("name", "Не указан") if isinstance(data.get("employer"), dict) else data.get("employer", "Не указан"),
            experience=data.get("experience", {}).get("name", "Не указан") if isinstance(data.get("experience"), dict) else data.get("experience", "Не указан"),
            schedule=data.get("schedule", {}).get("name", "Не указан") if isinstance(data.get("schedule"), dict) else data.get("schedule", "Не указан"),
        )

    def __str__(self):
        salary_info = (
            f"{self.salary.get('from', 'Не указано')} - {self.salary.get('to', 'Не указано')} {self.salary.get('currency', '')}"
            if self.salary else "Не указана"
        )
        return f"{self.name} ({self.area}) - {salary_info}\n{self.url}\n"

    def to_dict(self):
        """ Преобразует объект в словарь для сохранения в JSON """
        return {
            "id": self.id,
            "name": self.name,
            "salary": self.salary,
            "area": self.area,
            "published_at": self.published_at,
            "url": self.url,
            "employer": self.employer,
            "experience": self.experience,
            "schedule": self.schedule
        }

    def get_salary(self):
        """ Возвращает верхнюю границу зарплаты, если есть, иначе нижнюю """
        if self.salary:
            return self.salary.get("to") or self.salary.get("from") or 0
        return 0

    def sort_by_salary(vacancies, reverse=True):
        """ Сортирует вакансии по зарплате """
        return sorted(vacancies, key=lambda v: v.get_salary(), reverse=reverse)

    @staticmethod
    def filter_by_salary(vacancies, min_salary):
        """Фильтрует вакансии по минимальной зарплате"""
        filtered_vacancies = []
        for vacancy in vacancies:
            # Если vacancy – это словарь, преобразуем его в объект Vacancy
            if isinstance(vacancy, dict):
                vacancy = Vacancy.from_api_response(vacancy)

            # Проверяем, есть ли информация о зарплате
            if vacancy.salary and vacancy.salary.get("from"):
                salary_from = vacancy.salary["from"]
                if salary_from and salary_from >= min_salary:
                    filtered_vacancies.append(vacancy)

        return filtered_vacancies

    @staticmethod
    def sort_by_date(vacancies, reverse=True):
        """Сортирует вакансии по дате публикации (по убыванию, если reverse=True)."""
        return sorted(vacancies, key=lambda v: datetime.fromisoformat(v.published_at), reverse=reverse)

    @staticmethod
    def filter_by_city(vacancies, city: str):
        """Фильтрует вакансии по городу (регистр игнорируется)."""
        return [vac for vac in vacancies if vac.area.lower() == city.lower()]

    @staticmethod
    def filter_by_experience(vacancies, experience: str):
        """Фильтрует вакансии по требуемому опыту."""
        return [vac for vac in vacancies if vac.experience.lower() == experience.lower()]