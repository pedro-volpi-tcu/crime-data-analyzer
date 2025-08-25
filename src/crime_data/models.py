import pandas as pd

from . import config


class CrimeData:
    """
    Represents the raw crime data from all available years and
    provides methods to process it.
    """

    def __init__(self, data: pd.DataFrame):
        self._data = data

    @property
    def data(self) -> pd.DataFrame:
        """Returns the original, raw DataFrame."""
        return self._data

    def _to_numeric(self, df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
        for col in numeric_cols:
            if col in df.columns:
                if df[col].dtype == "object":
                    df[col] = df[col].str.replace(",", ".", regex=False)
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df[numeric_cols] = df[numeric_cols].fillna(0)

        return df

    def _filter_cols(self, df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
        return df[~df["evento"].isin(cols)]

    def get_processed_data(self) -> pd.DataFrame:
        """
        Cleans and aggregates the raw data to prepare it for analysis.

        Returns:
            pd.DataFrame: A new DataFrame grouped by crime type ('evento')
                          with cleaned, summed numeric columns.
        """
        if self._data.empty:
            return pd.DataFrame()

        # Work on a copy to keep the original data intact
        df = self._data.copy()

        # Filter non crime events
        df = self._filter_cols(df, config.NON_CRIME_EVENTS)

        # --- 1. Clean the Data ---
        df = self._to_numeric(df, config.NUMERIC_COLS)

        # --- 2. Aggregate the Data ---
        processed_df = df.groupby("evento")[config.NUMERIC_COLS].sum().reset_index()
        processed_df = processed_df.rename(columns={"evento": "crime_type"})

        return processed_df

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        num_rows, num_cols = self._data.shape
        memory_usage = self._data.memory_usage(deep=True).sum() / (1024**2)
        try:
            start_year = int(self._data["ano"].min())
            end_year = int(self._data["ano"].max())
            year_range = f", Anos: {start_year}-{end_year}"
        except (KeyError, TypeError, ValueError):
            year_range = ""
        return (
            f"<{class_name}: {num_rows:,} linhas, {num_cols} colunas" f"{year_range}, Memória: {memory_usage:.2f} MB>"
        )
