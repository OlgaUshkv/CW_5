import psycopg2
from psycopg2 import extensions


class DBManager:

    def __init__(self, host, dbname, user, password, port):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port
        self.connection: extensions.connection | None = None

    def connect(self):
        if self.connection is None:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port
            )

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_companies_and_vacancies_count(self):
        if self.connection is not None:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute('''
                    SELECT name, open_vacancies FROM employer
                ''')
                return cur.fetchall()

    def get_all_vacancies(self):
        if self.connection is not None:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute('''
                    SELECT emp.name, vac.name, (salary_from + salary_to)/2 as avg_sal, vac.url 
                    FROM vacancies as vac
                    left join employer as emp on vac.emp_id = emp.emp_id  
                    where salary_from is not null and salary_to is not null
                ''')
                return cur.fetchall()

    def get_avg_salary(self):
        if self.connection is not None:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute('''
                    SELECT AVG((salary_from + salary_to)/2) as avg_sal FROM vacancies
                    where salary_from is not null and salary_to is not null
                ''')
                return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        if self.connection is not None:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute('''
                    SELECT emp.name, vac.name, (salary_from + salary_to)/2 as avg_salary 
                    FROM vacancies as vac
                    left join employer as emp on vac.emp_id = emp.emp_id
                    where (salary_from + salary_to)/2 > (SELECT AVG((salary_from + salary_to)/2) as avg_sal 
                    FROM vacancies)
                ''')
                return cur.fetchall()

    def get_vacancies_with_keyword(self, search_word):
        word = f'%{search_word}%'
        if self.connection is not None:
            self.connect()
            with self.connection.cursor() as cur:
                cur.execute(f"SELECT emp.name, vac.name, (salary_from + salary_to)/2 as avg_sal "
                            f"FROM vacancies as vac "
                            f"Left join employer as emp on emp.emp_id = vac.emp_id "
                            f"where lower(vac.name) like (lower('{word}'))")
                return cur.fetchall()
