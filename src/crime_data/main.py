import argparse
import logging

from utils import config, log

from .loader import CrimeDataLoader
from .models import CrimeData
from .reporter import ReportDispatcher
from .scorer import AnalysisRunner, SeverityAnalyzer
from .serializer import CrimeDataSerializer

log.setup_logging()
logger = logging.getLogger(__name__)


def handle_cli_args() -> None:
    parser = argparse.ArgumentParser(description="Ferramenta para analisar dados de segurança pública.")
    parser.add_argument(
        "--clear",
        action="store_true",  # Transforma o argumento em uma flag booleana
        help="Apaga o arquivo de dados serializado para forçar uma reconstrução a partir da fonte.",
    )
    args = parser.parse_args()

    if args.clear:
        logger.info(f"Argumento --clear detectado. Tentando apagar '{config.SERIALIZE_FILEPATH}'...")
        try:
            if config.SERIALIZE_FILEPATH.exists():
                config.SERIALIZE_FILEPATH.unlink()  # Apaga o arquivo
                logger.info("Arquivo serializado apagado com sucesso.")
            else:
                logger.info("Nenhum arquivo serializado para apagar.")
        except OSError as e:
            logger.error(f"Impossível apagar o arquivo: {e}")


def load_or_build_data() -> CrimeData:
    logger.info("--- Iniciando carregamento de dados de Política Criminal ---")

    if not config.SERIALIZE_FILEPATH.exists():
        logger.info("Arquivo processado não encontrado. Construindo dados a partir da fonte...")
        loader = CrimeDataLoader(config.INPUT_DIR)
        crime_data = loader.load()

        logger.info(f"Salvando dados processados para uso futuro em '{config.SERIALIZE_FILEPATH}'...")
        CrimeDataSerializer.serialize(crime_data, config.SERIALIZE_FILEPATH)

        return crime_data

    logger.info(f"Arquivo processado encontrado em '{config.SERIALIZE_FILEPATH}'. Carregando...")
    return CrimeDataSerializer.deserialize(config.SERIALIZE_FILEPATH)


def perform_analysis(crime_data: CrimeData) -> None:
    reporter = ReportDispatcher()
    runner = AnalysisRunner()

    # runner.register(DrugSeizureByStateAnalyzer())
    # runner.register(FirearmSeizureByStateAnalyzer())
    # runner.register(GenderOfVictimsAnalyzer())
    # runner.register(LethalCrimesByStateAnalyzer())
    # runner.register(SeverityAnalyzer())
    analyzer = SeverityAnalyzer()  # The analyzer is now self-contained
    final_results_df = analyzer.analyze(crime_data)  # Pass the processed df
    logger.info(final_results_df.to_string())

    # runner.run(crime_data)
    # reporter.process_reports(runner.results)


def run() -> None:
    handle_cli_args()
    crime_data = load_or_build_data()
    perform_analysis(crime_data)


if __name__ == "__main__":
    run()
