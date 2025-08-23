import logging
import os
from typing import List
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv

from utils.api import handle_api_errors
from utils.log import setup_logging

from . import config
from .models import BaseExpense, OrganizationalExpense, ProgrammaticExpense

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

    @handle_api_errors(logger=logger)
    def fetch_expenses_by_agency(
        self, year: int, superior_organ: int, organ: int, page: int = 1
    ) -> List[OrganizationalExpense] | None:
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
            expenses = [OrganizationalExpense.from_api_dict(item) for item in response.json()]
            return expenses
        return None

    @handle_api_errors(logger=logger)
    def fetch_programatic_expenses(
        self,
        year: int,
        function_code: str | None,
        subfunction_code: str | None,
        program_code: str | None,
        action_code: str | None,
        page: int = 1,
    ) -> List[ProgrammaticExpense] | None:
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
            expenses = [ProgrammaticExpense.from_api_dict(item) for item in response.json()]
            return expenses
        return None


def log_expenses(title: str, expenses: list[BaseExpense]) -> None:
    logger.info(f"--- Logging {title} ---")
    for exp in expenses:
        if exp.empenhado:
            logger.info(exp)


if __name__ == "__main__":
    try:
        logger.info("--- Initializing API Client ---")

        client = TransparenciaApiClient()
        # expenses = client.fetch_expenses_by_agency(year=2024, superior_organ=30000, organ=30000, page=1)

        drug_policy_expenses = client.fetch_programatic_expenses(
            year=2025,
            function_code=None,
            subfunction_code=None,
            program_code="5115",
            action_code="20IE",
            page=1,
        )
        log_expenses(title="Política Pública sobre Drogas", expenses=drug_policy_expenses)

        public_safety_expenses = client.fetch_programatic_expenses(
            year=2025,
            function_code="06",
            subfunction_code=None,
            program_code=None,
            action_code=None,
            page=1,
        )
        log_expenses(title="Segurança Pública", expenses=public_safety_expenses)

    except ValueError as e:
        logger.critical(e)
