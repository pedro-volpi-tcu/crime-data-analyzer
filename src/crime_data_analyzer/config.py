# coding=utf-8
from pathlib import Path

ROOT = Path.cwd()

INPUT_DIR = ROOT / Path('data/input/')
OUTPUT_DIR = ROOT / Path('data/output/')

SERIALIZE_FILEPATH = OUTPUT_DIR / Path('crimedata.parquet')
