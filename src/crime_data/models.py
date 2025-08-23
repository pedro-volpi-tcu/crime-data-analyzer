import pandas as pd


class CrimeData:
    """
    Representa os dados do VDE em todos anos disponíveis.
    """

    def __init__(self, data: pd.DataFrame):
        self._data = data

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    def __repr__(self) -> str:
        # Coleta as informações básicas
        class_name = self.__class__.__name__
        num_rows, num_cols = self._data.shape
        memory_usage = self._data.memory_usage(deep=True).sum() / (1024**2)  # em MB

        # Tenta obter o intervalo de anos, se a coluna 'ano' existir
        try:
            start_year = self._data["ano"].min()
            end_year = self._data["ano"].max()
            year_range = f", Anos: {start_year}-{end_year}"
        except (KeyError, TypeError):
            year_range = ""  # Não mostra nada se a coluna não existir ou estiver vazia

        return (
            f"<{class_name}: {num_rows:,} linhas, {num_cols} colunas" f"{year_range}, Memória: {memory_usage:.2f} MB>"
        )
