from utils import log

from .analysis import (
    AnalysisRunner,
    DrugSeizureByStateAnalyzer,
    FirearmSeizureByStateAnalyzer,
    GenderOfVictimsAnalyzer,
    LethalCrimesByStateAnalyzer,
    VehicleCrimeByStateAnalyzer,
)
from .cli import handle_cli_args
from .data_manager import load_or_build_data
from .models import CrimeData
from .reporter import ReportDispatcher

log.setup_logging()


def perform_analysis(crime_data: CrimeData) -> None:
    reporter = ReportDispatcher()
    runner = AnalysisRunner()

    runner.register(DrugSeizureByStateAnalyzer())
    runner.register(FirearmSeizureByStateAnalyzer())
    runner.register(GenderOfVictimsAnalyzer())
    runner.register(LethalCrimesByStateAnalyzer())
    runner.register(VehicleCrimeByStateAnalyzer())

    runner.run(crime_data)
    reporter.process_reports(runner.results)


def run() -> None:
    handle_cli_args()

    crime_data = load_or_build_data()
    perform_analysis(crime_data)


if __name__ == "__main__":
    run()
