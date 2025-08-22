import logging
import os
from typing import List
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from utils.log import setup_logging

from . import config
from .models import ExpenseResponse

load_dotenv()
setup_logging()
logger = logging.getLogger(__name__)


class TransparenciaApiClient:
    """
    A client for interacting with the Portal da Transparência API.
    """

    def __init__(self) -> None:
        self.base_url = config.URL_PORTAL_TRANSPARENCIA

        self._api_key = os.getenv("KEY_VALUE")
        self._api_key_name = os.getenv("KEY_NAME")

        if not self._api_key:
            logger.error("API Key not found. Provide it or set KEY_VALUE in your .env file.")
            raise ValueError("API Key is missing.")

        # Create a session to persist headers and improve performance
        self.session = requests.Session()
        self.session.headers.update({self._api_key_name: self._api_key, "accept": "*/*"})

    def fetch_expenses_by_agency(
        self, year: int, superior_organ: int, organ: int, page: int = 1
    ) -> ExpenseResponse | None:
        """
        Fetches expense data for a given year.
        """
        ##########################################################################################
        #  WARNING: NÃO PODE TER FORWARD SLASH ('/') NEM NO INÍCIO NEM NO FIM DESSE ENDPOINT!!!  #
        ##########################################################################################
        endpoint = r"despesas/por-orgao"
        url = urljoin(self.base_url, endpoint)

        params = {"ano": year, "orgaoSuperior": superior_organ, "orgao": organ, "pagina": page}

        logger.info(f"Requesting expenses for {year} from {url} for {superior_organ}/{organ}")

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            logger.info(f"Successfully fetched {len(response.json())} expense records.")
            return ExpenseResponse(**response.json())

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for year {year}: {e}")
            return None


if __name__ == "__main__":
    try:
        logger.info("--- Initializing API Client ---")

        client = TransparenciaApiClient()
        expenses = client.fetch_expenses_by_agency(year=2024, superior_organ=30000, organ=30000, page=1)

        if expenses:
            logger.info(expenses)
        else:
            logger.critical("No response returned!")

    except ValueError as e:
        logger.critical(e)
