from pathlib import Path

import pandas as pd

from .models import CrimeData


class CrimeDataSerializer:
    @staticmethod
    def serialize(crime_data_obj: CrimeData, path: Path) -> None:
        print(f"Serializando objeto para {path}...")
        crime_data_obj.data.to_parquet(path, index=False)
        print("Serializado com sucesso.")

    @staticmethod
    def deserialize(path: Path) -> CrimeData:
        print(f"Desserializando dados de {path}...")
        if not Path(path).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        data = pd.read_parquet(path)
        print("Desserializado com sucesso.")
        return CrimeData(data)
