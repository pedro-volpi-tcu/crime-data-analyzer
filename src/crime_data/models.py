import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import pandas as pd

from utils import config


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

        # Rename some cols
        processed_df = df.rename(
            columns={
                "total_vitima": "victims",
                "total_peso": "weight",
                "total": "aprehensions",
            }
        )

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


@dataclass
class CrimeEvent:
    name: str
    victims: int
    weight: float
    aprehensions: int

    W: dict[str, float] = {"victims": 0.6, "weight": 0.3, "aprehensions": 0.1}
    # Composition: The context is a dictionary mapping metric keys to category objects.
    statistical_context: dict[str, "BaseCategory"] = field(default_factory=dict, repr=False)

    def z_transform(self, metric_name: str) -> float:
        """Calculates the Z-score of a metric."""

        raw_value: int | float = getattr(self, metric_name, 0.0)

        stats = self.statistical_context.get(metric_name)

        if not stats or stats.stdev == 0:
            return 0.0
        return (raw_value - stats.mean) / stats.stdev

    @property
    def severity(self) -> float:
        return (
            CrimeEvent.W["victims"] * self.z_transform("victims")
            + CrimeEvent.W["weight"] * self.z_transform("weights")
            + CrimeEvent.W["aprehensions"] * self.z_transform("aprehensions")
        )


class BaseCategory(ABC):
    """
    An abstract base class for a category of metrics.

    It stores the raw values and calculates total, N, mean, and standard
    deviation on the fly.
    """

    def __init__(self, values: list[int | float]):
        self._values = values

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @property
    def N(self) -> int:
        """The number of records."""
        return len(self._values)

    @property
    def total(self) -> int | float:
        """The total sum of the metric's values."""
        return sum(self._values)

    @property
    def mean(self) -> float:
        """The average (mean) of the values."""
        if self.N == 0:
            return 0.0
        return float(self.total / self.N)

    @property
    def stdev(self) -> float:
        """The population standard deviation of the values."""
        if self.N <= 1:  # Standard deviation requires at least two points
            return 0.0
        mean = self.mean
        variance = sum((x - mean) ** 2 for x in self._values) / self.N
        return math.sqrt(variance)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(Total={self.total}, N={self.N}, "
            f"Mean={self.mean:.2f}, StDev={self.stdev:.2f})"
        )


class VictimCategory(BaseCategory):
    @property
    def name(self) -> str:
        return "victims"


class WeightCategory(BaseCategory):
    @property
    def name(self) -> str:
        return "weights"


class AprehensionCategory(BaseCategory):
    @property
    def name(self) -> str:
        return "aprehensions"
