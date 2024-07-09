from C_WORK_5.api_clients.base_api import APIClient
from C_WORK_5.api_clients.employer_info import Employer
from C_WORK_5.api_clients.vacancy_info import Vacancy


class HHAPIClient(APIClient):
    def __init__(self):
        self.__base_url = 'https://api.hh.ru/'

    @property
    def base_url(self) -> str:
        return self.__base_url

    def search_employers(self, search: str, *, only_with_vacancies=True) -> list[Employer]:
        params = {
            'text': search,
            'only_with_vacancies': only_with_vacancies
        }
        employers = self.get_items('/employers', params=params)
        return [
            Employer(
                id=int(emp['id']),
                name=emp['name'],
                url=emp['alternate_url'],
                open_vacancies=emp['open_vacancies']
            )
            for emp in employers
        ]

    def search_vacancies(self, employer_id: int) -> list[Vacancy]:
        params = {
            'employer_id': employer_id,
            'only_with_salary': True
        }
        vacancies = self.get_items('/vacancies', params=params)
        return [
            Vacancy(id=int(vac['id']),
                    employer_id=employer_id,
                    name=vac['name'],
                    url=vac['alternate_url'],
                    area=vac['area'].get('name'),
                    salary_from=vac['salary'].get('from'),
                    salary_to=vac['salary'].get('to')
                    )
            for vac in vacancies
        ]

    def get_items(self, url: str, params: dict) -> list[dict]:
        items = []
        params['page'] = 0
        params['per_pages'] = 100
        while True:
            data = self.get(url, params=params)
            items.extend(data['items'])

            total_pages = data['pages']
            if total_pages == params['page']:
                break
            params['page'] += 1

            if len(items) >= 2000:
                break

        return items
