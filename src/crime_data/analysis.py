import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal

import pandas as pd

from .models import CrimeData

ResultType = Literal["table", "bar_chart", "csv"]

logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Container para o output das análises."""

    name: str
    description: str
    data: pd.DataFrame
    requested_formats: list[ResultType] = field(default_factory=lambda: ["table"])


class Analyzer(ABC):
    """Abstract Base Class to define the Analyzer interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the analysis."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        """Runs the analysis and returns a DataFrame with the results."""
        pass


class LethalCrimesByStateAnalyzer(Analyzer):
    """Agrega os principais crimes letais para criar um ranking de estados."""

    @property
    def name(self) -> str:
        return "Ranking de Vítimas de Crimes Letais por Estado"

    @property
    def description(self) -> str:
        return "Soma o total de vítimas de Homicídio Doloso, Feminicídio, Latrocínio e Lesão Corporal Seguida de Morte por UF."

    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        logger.info(f"Executando análise: {self.name}...")
        try:
            lethal_events = [
                "Homicídio doloso",
                "Feminicídio",
                "Roubo seguido de morte (latrocínio)",
                "Lesão corporal seguida de morte",
            ]
            filtered_df = crime_data.data[crime_data.data["evento"].isin(lethal_events)]

            # Usamos 'total_vitima' pois é a métrica mais relevante para esses crimes
            result = filtered_df.groupby("uf")["total_vitima"].sum().sort_values(ascending=False).reset_index()
            result = result.rename(columns={"uf": "UF", "total_vitima": "Total de Vítimas Letais"})

            return AnalysisResult(self.name, self.description, result, ["bar_chart"])

        except KeyError:
            logger.warning(f"Colunas necessárias não encontradas para '{self.name}'.")
            return AnalysisResult(self.name, self.description, pd.DataFrame())


class DrugSeizureByStateAnalyzer(Analyzer):
    """Analisa o peso total de Cocaína e Maconha apreendidos por estado."""

    @property
    def name(self) -> str:
        return "Ranking de Apreensão de Drogas (kg) por Estado"

    @property
    def description(self) -> str:
        return (
            "Soma o peso (em kg) de Cocaína e Maconha apreendidos, ranqueando os estados com maiores apreensões totais."
        )

    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        logger.info(f"Executando análise: {self.name}...")

        try:
            drug_events = ["Apreensão de Cocaína", "Apreensão de Maconha"]
            filtered_df = crime_data.data[crime_data.data["evento"].isin(drug_events)]

            # Pivot table para ver os totais de cada droga lado a lado
            pivot_df = filtered_df.pivot_table(index="uf", columns="evento", values="total_peso", aggfunc="sum").fillna(
                0
            )

            pivot_df["Total Apreendido (kg)"] = pivot_df.sum(axis=1)
            result = pivot_df.sort_values(by="Total Apreendido (kg)", ascending=False).reset_index()
            result = result.rename(columns={"uf": "UF"})

            return AnalysisResult(self.name, self.description, result)

        except KeyError:
            logger.warning(f"Colunas necessárias não encontradas para '{self.name}'.")
            return AnalysisResult(self.name, self.description, pd.DataFrame())


class FirearmSeizureByStateAnalyzer(Analyzer):
    """Cria um ranking de estados pela quantidade de armas de fogo apreendidas."""

    @property
    def name(self) -> str:
        return "Ranking de Apreensão de Armas de Fogo por Estado"

    @property
    def description(self) -> str:
        return "Soma o total de armas de fogo apreendidas por UF, um indicador da atividade policial contra o crime armado."

    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        logger.info(f"Executando análise: {self.name}...")

        try:
            event_name = "Arma de Fogo Apreendida"
            filtered_df = crime_data.data[crime_data.data["evento"] == event_name]

            # TODO: agrupar por tipo de arma?
            result = filtered_df.groupby("uf")["total"].sum().sort_values(ascending=False).reset_index()
            result = result.rename(columns={"uf": "UF", "arma": "Tipo de arma"})

            return AnalysisResult(self.name, self.description, result)

        except KeyError:
            logger.info(f"  -> Aviso: Colunas necessárias não encontradas para '{self.name}'.")
            return AnalysisResult(self.name, self.description, pd.DataFrame())


class VehicleCrimeByStateAnalyzer(Analyzer):
    """Agrega dados de roubo e furto de veículos por estado."""

    @property
    def name(self) -> str:
        return "Ranking de Roubo e Furto de Veículos por Estado"

    @property
    def description(self) -> str:
        return "Soma o total de eventos de 'Roubo de veículo' e 'Furto de veículo' por UF."

    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        logger.info(f"Executando análise: {self.name}...")
        try:
            vehicle_events = ["Roubo de veículo", "Furto de veículo"]
            filtered_df = crime_data.data[crime_data.data["evento"].isin(vehicle_events)]

            # A coluna 'total' deve conter o número de eventos
            result = filtered_df.groupby("uf")["total"].sum().sort_values(ascending=False).reset_index()
            result = result.rename(columns={"uf": "UF", "total": "Total de Veículos (Roubo/Furto)"})

            return AnalysisResult(self.name, self.description, result)
        except KeyError:
            logger.info(f"  -> Aviso: Colunas necessárias não encontradas para '{self.name}'.")
            return AnalysisResult(self.name, self.description, pd.DataFrame())


class GenderOfVictimsAnalyzer(Analyzer):
    """Analisa a divisão por gênero de vítimas em crimes violentos selecionados."""

    @property
    def name(self) -> str:
        return "Divisão de Gênero das Vítimas (Crimes Violentos)"

    @property
    def description(self) -> str:
        return "Soma o total de vítimas masculinas e femininas para Homicídio Doloso e Tentativa de Homicídio."

    def analyze(self, crime_data: CrimeData) -> AnalysisResult:
        logger.info(f"Executando análise: {self.name}...")
        try:
            violent_events = ["Homicídio doloso", "Tentativa de homicídio"]
            filtered_df = crime_data.data[crime_data.data["evento"].isin(violent_events)]

            # Soma as colunas de gênero
            total_feminino = filtered_df["feminino"].sum()
            total_masculino = filtered_df["masculino"].sum()

            result = pd.DataFrame(
                {
                    "Gênero": ["Feminino", "Masculino"],
                    "Total de Vítimas": [total_feminino, total_masculino],
                }
            )

            return AnalysisResult(self.name, self.description, result)

        except KeyError:
            logger.warning(f"Colunas necessárias não encontradas para '{self.name}'.")
            return AnalysisResult(self.name, self.description, pd.DataFrame())


class AnalysisRunner:
    """Manages and runs a series of analyzer objects."""

    def __init__(self) -> None:
        self._analyzers: list[Analyzer] = []
        self.results: list[AnalysisResult] = []

    def register(self, analyzer: Analyzer) -> None:
        """Adds an analyzer to the run list."""
        self._analyzers.append(analyzer)
        logger.info(f"Analisador '{analyzer.name}' registrado.")

    def run(self, crime_data: CrimeData) -> None:
        """Runs all registered analyzers on the given CrimeData."""
        logger.info("--- Iniciando Análises de Política Criminal ---")

        if not self._analyzers:
            logger.info("Nenhum analisador registrado.")
            return

        for analyzer in self._analyzers:
            self.results.append(analyzer.analyze(crime_data))
        logger.info("--- Análises Concluídas ---")
