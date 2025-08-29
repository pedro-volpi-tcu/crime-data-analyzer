import logging
from pathlib import Path
from typing import List

import pandas as pd
import regex as re

from .models import AprehensionCategory, BaseCategory, CrimeData, CrimeEvent, VictimCategory, WeightCategory

logger = logging.getLogger(__name__)


class CrimeDataBuilder:
    def __init__(self, source_dir: Path):
        self._source_dir = source_dir
        self._dataframes: List[pd.DataFrame] = []

    def _process_file(self, filepath: Path) -> pd.DataFrame:
        """
        Abstrai o processamento de um único arquivo Excel.
        """
        logger.info(f"Processando arquivo: {filepath.name}...")

        df = pd.read_excel(filepath, sheet_name=0)
        try:
            year = self._get_year_from_file(filepath)
            df["ano"] = year
        except ValueError:
            logger.error(
                f"Aviso: Não foi possível extrair o ano do nome do arquivo {filepath.name}. "
                f"A coluna 'ano' não será adicionada para este arquivo."
            )
        return df

    def _get_year_from_file(self, filepath: Path) -> int:
        filename = filepath.stem
        pat = r"\d{4}"
        if match := re.search(pat, filename):
            return int(match.group(0))
        raise ValueError

    def build(self) -> CrimeData:
        # Itera sobre todos os arquivos .xlsx no diretório
        xlsx_files = list(self._source_dir.glob("*.xlsx"))

        if not xlsx_files:
            logger.error(f"Aviso: Nenhum arquivo .xlsx encontrado em {self._source_dir}")
            return CrimeData(pd.DataFrame())

        self._dataframes = [self._process_file(f) for f in xlsx_files]

        # Concatena todos os DataFrames em um só
        full_df = pd.concat(self._dataframes, ignore_index=True)

        return CrimeData(full_df)


class CrimeEventsBuilder:
    """Receives a processed dataframe (grouped by 'crime_type') and returns a list of CrimeEvent objects."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def build(self) -> list[CrimeEvent]:
        events: list[CrimeEvent] = []
        for row in self._df.itertuples(index=False):
            try:
                event = CrimeEvent(
                    name=getattr(row, "crime_type"),
                    victims=getattr(row, "victims", 0),
                    weight=getattr(row, "weight", 0.0),
                    aprehensions=getattr(row, "aprehensions", 0),
                )
                events.append(event)

            except (AttributeError, TypeError, ValueError) as e:
                logger.critical(f"Skipping malformed Dataframe row: {row}. Error: {e}")

        return events


class CrimeCategoryBuilder:
    """Receives a list of CrimeEvent objects and returns a dict of each crime category aggregate."""

    def __init__(self, events: list[CrimeEvent]) -> None:
        self._events = events

    def build(self) -> dict[str, BaseCategory]:
        logger.info("--- Building aggregate Category objects from list of CrimeEvents. ---")

        return {
            "victims": VictimCategory([e.victims for e in self._events]),
            "weight": WeightCategory([e.weight for e in self._events]),
            "aprehensions": AprehensionCategory([e.aprehensions for e in self._events]),
        }
