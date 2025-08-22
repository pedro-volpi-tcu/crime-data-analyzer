import logging
import os
from typing import List
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from utils.api import handle_api_errors
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

    @handle_api_errors
    def fetch_expenses_by_agency(
        self, year: int, superior_organ: int, organ: int, page: int = 1
    ) -> List[ExpenseResponse] | None:
        """
        Fetches expense data for a given year, for a given organ.
        """
        ##########################################################################################
        #  WARNING: NÃO PODE TER FORWARD SLASH ('/') NEM NO INÍCIO NEM NO FIM DESSE ENDPOINT!!!  #
        ##########################################################################################
        endpoint = r"despesas/por-orgao"
        url = urljoin(self.base_url, endpoint)

        params = {"ano": year, "orgaoSuperior": superior_organ, "orgao": organ, "pagina": page}

        logger.info(f"Requesting expenses for {year} from {url} for {superior_organ}/{organ}")

        response = self.session.get(url, params=params)
        response.raise_for_status()
        if n := len(response.json()):
            logger.info(f"Successfully fetched {n} expense records.")
            expenses = [ExpenseResponse.from_api_dict(item) for item in response.json()]
            return expenses
        return None

    def fetch_programatic_expenses(
        self, year: int, function_code: str, subfunction_code: str, program_code: str, action_code: str, page: int = 1
    ) -> List[ExpenseResponse] | None:
        """
        Fetches programatic expense data.
        """
        endpoint = r"despesas/por-funcional-programatica"
        url = urljoin(self.base_url, endpoint)

        params = {
            "ano": year,
            "funcao": function_code,
            "subfuncao": subfunction_code,
            "programa": program_code,
            "acao": action_code,
            "pagina": page,
        }

        response = self.session.get(url, params=params)
        if n := len(response.json()):
            logger.info(f"Successfully fetched {n} expense records.")
            expenses = [ExpenseResponse.from_api_dict(item) for item in response.json()]
            return expenses
        return None


if __name__ == "__main__":
    try:
        logger.info("--- Initializing API Client ---")

        client = TransparenciaApiClient()
        for page_num in range(1, 10):
            expenses = client.fetch_expenses_by_agency(year=2024, superior_organ=30000, organ=30000, page=page_num)

            if expenses:
                logger.info(expenses)
            else:
                logger.warning("No response returned!")

    except ValueError as e:
        logger.critical(e)
