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

    @classmethod
    def from_api_response(cls, data: dict):
        """ Создает объект Vacancy из ответа API """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            salary=data.get("salary", {}),
            area=data.get("area", {}).get("name", "Не указан"),
            published_at=data.get("published_at"),
            url=data.get("alternate_url"),
            employer={
                "name" : data.get("employer", {}).get("name", "Не указан"),
                "url" : data.get("employer", {}).get("alternate_url", "#")
            },
            experience=data.get("experience", {}).get("name", "Не указан"),
            schedule=data.get("schedule", {}).get("name", "Не указан"),
        )

    def __str__(self):
        salary_info = (
            f"{self.salary.get('from', 'Не указано')} - {self.salary.get('to', 'Не указано')} {self.salary.get('currency', '')}"
            if self.salary else "Не указана"
        )
        return f"{self.name} ({self.area}) - {salary_info}\n{self.url}\n"

    def get_salary(self):
        """ Возвращает верхнюю границу зарплаты, если есть, иначе нижнюю """
        if self.salary:
            return self.salary.get("to") or self.salary.get("from") or 0
        return 0

    @staticmethod
    def filter_by_salary(vacancies, min_salary):
        """ Фильтрует вакансии по минимальной зарплате """
        return [vac for vac in vacancies if vac.get_salary() >= min_salary]

