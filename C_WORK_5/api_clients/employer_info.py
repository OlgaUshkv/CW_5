from dataclasses import dataclass


@dataclass
class Employer:
    id: int
    name: str
    url: str
    open_vacancies: int
