from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

INPUT_DIR = ROOT_DIR / Path("data/input/")
OUTPUT_DIR = ROOT_DIR / Path("data/output/")

SERIALIZE_FILEPATH = OUTPUT_DIR / Path("crimedata.parquet")
