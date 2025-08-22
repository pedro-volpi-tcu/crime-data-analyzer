import logging
import os
from typing import List
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from utils.log import setup_logging

from .models import ExpenseResponse

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


class TransparenciaApiClient:
    """
    A client for interacting with the Portal da Transparência API.
    """

    def __init__(self) -> None:
        self.base_url = "https://api-d.portaldatransparencia.gov.br/api-de-dados"

        self._api_key = os.getenv("KEY_VALUE")
        self._api_key_name = os.getenv("KEY_NAME")

        print(f"{self._api_key_name}: {self._api_key}")

        if not self._api_key:
            logger.error("API Key not found. Provide it or set KEY_VALUE in your .env file.")
            raise ValueError("API Key is missing.")

        # Create a session to persist headers and improve performance
        self.session = requests.Session()
        self.session.headers.update({self._api_key_name: self._api_key})

    def fetch_expenses_by_agency(self, year: int, page: int = 1) -> List[ExpenseResponse]:
        """
        Fetches expense data for a given year.

        Args:
            year: The year to query.
            page: The page number for pagination.

        Returns:
            A list of dictionaries representing the expense records.
        """
        endpoint = "/despesas/por-orgao"
        url = urljoin(self.base_url, endpoint)

        params = {"ano": year, "pagina": page}

        logger.info(f"Requesting expenses for {year} from {url}")
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            logger.info(f"Successfully fetched {len(response.json())} expense records.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for year {year}: {e}")
            return []


if __name__ == "__main__":
    try:
        logger.info("--- Initializing API Client ---")
        # 1. Create an instance of the client
        client = TransparenciaApiClient()

        # 2. Call a method on the instance
        expenses_2024 = client.fetch_expenses_by_agency(year=2024, page=1)

        if expenses_2024:
            logger.info(expenses_2024)
        else:
            logger.warning("Fetch returned no data.")

    except ValueError as e:
        logger.critical(e)
