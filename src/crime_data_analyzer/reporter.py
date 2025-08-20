# coding=utf-8
import logging
from abc import ABC, abstractmethod

from . import config
from .analysis import AnalysisResult
from .plotter import BarPlotter


class ResultReporter(ABC):
    """
    Reporta os resultados das análises.
    """

    @abstractmethod
    def report(self, result: AnalysisResult) -> None:
        pass


class LogReporter(ResultReporter):
    """
    Reporta os resultados das análises no arquivo de log.
    """

    def report(self, result: AnalysisResult) -> None:
        logging.info("--- Relatório das análises ---")

        if result.data.empty:
            logging.warning(f"Nenhum resultado a reportar para {result.name}.")
            return

        logging.info(result.data.to_string(index=False))


class BarChartReporter(ResultReporter):
    """
    Cria um gráfico de barras a partir dos dados fornecidos.
    """

    def report(self, result: AnalysisResult) -> None:
        output_path = config.OUTPUT_DIR / f"{result.name}"
        plotter = BarPlotter()
        plotter.plot(result.data, result.name, output_path)


class ReportDispatcher:
    def __init__(self) -> None:
        self._reporters_map = {
            "table": LogReporter(),
            "bar_chart": BarChartReporter(),
        }

    def process_reports(self, results: list[AnalysisResult]) -> None:
        for idx, res in enumerate(results):
            logging.info(f"{50 * '='} {idx+1} {50 * '='}")
            logging.info(f"Análise: {res.name}")
            logging.info(f"Descrição: {res.description}")
            logging.info("=" * 50)
            logging.info(f"Processando análise: '{res.name}'")

            for format_type in res.requested_formats:
                if format_type not in self._reporters_map:
                    logging.warning(f"Nenhum reporter configurado para o formato '{format_type}'.")
                    continue

                reporter = self._reporters_map[format_type]
                reporter.report(res)
