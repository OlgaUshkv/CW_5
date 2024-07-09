import psycopg2

from C_WORK_5.api_clients.employer_info import Employer
from C_WORK_5.api_clients.vacancy_info import Vacancy


def create_databases(database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.commit()
    conn.close()


def create_schema(database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employer(
                emp_id integer PRIMARY KEY,
                name text NOT NULL,
                url text NOT NULL,
                open_vacancies integer NOT NULL
            )
            """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies(
                vac_id integer PRIMARY KEY,
                emp_id integer REFERENCES employer(emp_id),
                name text NOT NULL,
                url text NOT NULL,
                area text NOT NULL,
                salary_from integer,
                salary_to integer
            )
            """
        )

    conn.commit()
    conn.close()


def save_emp_to_database(data: Employer, database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        # for emp in data:
        cur.execute("""
               INSERT INTO employer (emp_id, name, url, open_vacancies)
               VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
        """, (data.id, data.name, data.url, data.open_vacancies))

    conn.commit()
    conn.close()


def save_vac_to_database(data: list[Vacancy], database_name: str, params: dict) -> None:
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vac in data:
            cur.execute("""
                INSERT INTO vacancies (vac_id, emp_id, name, url, area, salary_from, salary_to)
                VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
            """, (vac.id, vac.employer_id, vac.name, vac.url, vac.area, vac.salary_from, vac.salary_to))

    conn.commit()
    conn.close()
