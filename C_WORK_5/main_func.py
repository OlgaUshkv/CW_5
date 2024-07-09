from api_clients.hh_client import HHAPIClient
from db_pack.config import config
from db_pack.db_create import create_databases, create_schema, save_emp_to_database, save_vac_to_database


def first_step_function():
    params = config()

    create_databases('cw_5', params)
    create_schema('cw_5', params)

    list_company = ['лср', 'яндекс', 'VK', 'DNS', 'газпром нефть', 'точка', 'skypro', 'авито', 'setl group',
                    'okko']

    hh_client = HHAPIClient()

    for company in list_company:
        employers = hh_client.search_employers(company)
        max_zn = max([emp.open_vacancies for emp in employers])
        for emp in employers:
            if emp.open_vacancies == max_zn:
                save_emp_to_database(emp, 'cw_5', params)
                print(emp)
                vacancies = hh_client.search_vacancies(emp.id)
                save_vac_to_database(vacancies, 'cw_5', params)
                break
