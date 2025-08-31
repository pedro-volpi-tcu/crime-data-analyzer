from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = ROOT_DIR / Path("data/input/")
OUTPUT_DIR = ROOT_DIR / Path("data/output/")

SERIALIZE_FILEPATH = OUTPUT_DIR / Path("crimedata.parquet")

NUMERIC_COLS = ["feminino", "masculino", "nao_informado", "total_vitima", "total", "total_peso"]
NON_CRIME_EVENTS = [
    "Pessoa Localizada",
    "Emissão de Alvarás de licença",
    "Atendimento pré-hospitalar",
    "Realização de vistorias",
    "Busca e salvamento",
    "Mandado de prisão cumprido",
]
