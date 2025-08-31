import logging
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from tqdm import tqdm

from crime_data import config

EXCEL_FILE_PATH: Path = config.INPUT_DIR / "BancoVDE 2025.xlsx"
logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def dataframe_from_excel() -> pd.DataFrame:
    """
    Pytest fixture to load the DataFrame from a specified Excel file.
    """
    try:
        return pd.read_excel(EXCEL_FILE_PATH)
    except FileNotFoundError:
        pytest.fail(
            f"The specified Excel file was not found at '{EXCEL_FILE_PATH}'. "
            "Please ensure the path is correct and the file exists."
        )
    except Exception as e:
        pytest.fail(f"An error occurred while reading the Excel file: {e}")


def test_no_row_with_multiple_total_values(dataframe_from_excel: pd.DataFrame, capsys) -> None:
    """
    Tests that no row in the DataFrame has non-null values in more than one
    of the key 'total' columns, with a progress bar for large files.

    The validation checks if any row has data in at least two of the following
    columns simultaneously: 'total_vitima', 'total_peso', 'total'.
    """
    columns_to_check = ["total_vitima", "total_peso", "total"]

    missing_cols = [col for col in columns_to_check if col not in dataframe_from_excel.columns]
    if missing_cols:
        pytest.fail(f"The DataFrame is missing the following required columns: {missing_cols}")

    # --- Progress Bar Implementation ---
    # Define a chunk size for processing. Adjust based on your memory and file size.
    chunk_size = 100000
    num_chunks = int(np.ceil(len(dataframe_from_excel) / chunk_size))

    # Split the DataFrame into manageable chunks.
    df_chunks = np.array_split(dataframe_from_excel, num_chunks)

    all_invalid_rows = []

    # `capsys.disabled()` is used to temporarily disable pytest's output capturing,
    # allowing the tqdm progress bar to render correctly in the console during the test.
    with capsys.disabled():
        logger.info(f"\nProcessing {len(dataframe_from_excel):,} rows in {num_chunks} chunks...")
        for chunk in tqdm(df_chunks, desc="Validating DataFrame Chunks"):
            # The same validation logic is applied to each chunk
            non_null_counts = chunk[columns_to_check].notna().sum(axis=1)
            invalid_rows_in_chunk = chunk[non_null_counts >= 2]

            if not invalid_rows_in_chunk.empty:
                all_invalid_rows.append(invalid_rows_in_chunk)

    # After processing all chunks, combine any found invalid rows.
    if all_invalid_rows:
        invalid_rows = pd.concat(all_invalid_rows)
        num_invalid_rows = len(invalid_rows)
    else:
        num_invalid_rows = 0

    # The final assertion remains the same.
    assert num_invalid_rows == 0, (
        f"Validation Failed: Found {num_invalid_rows} row(s) with values in "
        f"more than one of the specified columns {columns_to_check}.\n"
        f"Problematic Rows (showing first 5):\n{invalid_rows.head(5)}"
    )
