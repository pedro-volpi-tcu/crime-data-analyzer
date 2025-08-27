import logging
from pathlib import Path

import pandas as pd

from .models import CrimeData

logger = logging.getLogger(__name__)


class CrimeDataSerializer:
    @staticmethod
    def serialize(crime_data_obj: CrimeData, path: Path) -> None:
        logger.info(f"Serializando objeto para {path}...")
        crime_data_obj.data.to_parquet(path, index=False)
        logger.info("Serializado com sucesso.")

    @staticmethod
    def deserialize(path: Path) -> CrimeData:
        logger.info(f"Desserializando dados de {path}...")
        if not Path(path).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        data = pd.read_parquet(path)
        logger.info("Desserializado com sucesso.")
        return CrimeData(data)
