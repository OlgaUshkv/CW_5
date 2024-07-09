from abc import ABC, abstractmethod

import requests


class APIClient(ABC):
    @property
    @abstractmethod
    def base_url(self) -> str:
        pass

    def get(self, url: str, params: dict) -> dict:
        full_url = self.base_url + url

        response = requests.get(full_url, params=params, timeout=3)
        response.raise_for_status()
        return response.json()
