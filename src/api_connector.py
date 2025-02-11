from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy


class APIConnector(ABC):
    @abstractmethod
    def get_data(self, endpoint: str, params: dict) -> dict:
        """ Получение данных из API. """
        pass

    @abstractmethod
    def connect(self) -> None:
        """ Подключение к API. """
        pass


class HeadHunterAPI(APIConnector):
    BASE_URL = "https://api.hh.ru/vacancies"

    def connect(self) -> None:
        """ Реализация подключения (если потребуется аутентификация). """
        pass

    def get_data(self, endpoint: str, params: dict) -> dict:
        """ Запрос данных по указанному эндпоинту API HeadHunter. """
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, search_text: str):
        params = {
            "text": search_text,
            "area": "1",
            "per_page": 20
        }
        print(f"DEBUG: Отправляем запрос в API с параметрами: {params}")

        response = requests.get(f"{self.BASE_URL}", params=params)

        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}, {response.text}")
            return []

        data = response.json()
        print(f"DEBUG: Получено {len(data.get('items', []))} вакансий")
        return data.get("items", [])