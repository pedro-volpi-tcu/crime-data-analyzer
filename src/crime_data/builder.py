# coding=utf-8
import logging
from pathlib import Path
from typing import List

import pandas as pd
import regex as re

from .models import CrimeData


class CrimeDataBuilder:
    def __init__(self, source_dir: Path):
        self._source_dir = source_dir
        self._dataframes: List[pd.DataFrame] = []

    def _process_file(self, filepath: Path) -> pd.DataFrame:
        """
        Abstrai o processamento de um único arquivo Excel.
        """
        logging.info(f"Processando arquivo: {filepath.name}...")

        df = pd.read_excel(filepath, sheet_name=0)
        try:
            year = self._get_year_from_file(filepath)
            df["ano"] = year
        except ValueError:
            logging.error(
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
            logging.error(f"Aviso: Nenhum arquivo .xlsx encontrado em {self._source_dir}")
            return CrimeData(pd.DataFrame())

        self._dataframes = [self._process_file(f) for f in xlsx_files]

        # Concatena todos os DataFrames em um só
        full_df = pd.concat(self._dataframes, ignore_index=True)

        return CrimeData(full_df)
