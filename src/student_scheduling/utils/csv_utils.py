"""Helper functions for handling CSV files"""

from io import StringIO

import magic
import pandas as pd

from config.logging import logger


def csv_has_csv_mime_type(content: bytes) -> bool:
    """Check if the uploaded file is a safe CSV file. This is the first layer of safety

    Args:
        content (bytes): The file to check in bytes.
    Returns:
        bool: True if the file is a safe CSV file, False otherwise.
    """

    max_file_size = 15 * 1024 * 1024  # 15 MB

    if len(content) > max_file_size:
        logger.warning(
            "csv_has_csv_mime_types: Uploaded file is greater than %.1fMB",
            max_file_size,
        )
        return False

    file_type = magic.from_buffer(content, mime=True)

    accepted_mimes = ["text/csv"]
    return file_type in accepted_mimes


def csv_has_2_columns(content: bytes) -> bool:
    """Check if the uploaded CSV file has exactly 2 columns. This is the second layer of safety.

    Args:
        content (bytes): The CSV file to check.
    Returns:
        bool: True if the file has exactly 2 columns, False otherwise.
    """

    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        return df.shape[1] == 2
    except Exception:
        logger.warning("csv_has_2_columns: CSV file doesn't have exactly 2 columns.")
        return False


def csv_is_safe(content: bytes) -> bool:
    """Check if the uploaded CSV file is safe by verifying its MIME type and column count.

    Args:
        content (bytes): The CSV file to check.
    Returns:
        bool: True if the file is safe, False otherwise.
    """
    safe_mime_type = csv_has_csv_mime_type(content)
    has_2_columns = csv_has_2_columns(content)
    is_safe = safe_mime_type and has_2_columns
    if not is_safe:
        logger.warning(
            "csv_is_safe: Safe MIME: %r, Exactly 2 columns: %r",
            safe_mime_type,
            has_2_columns,
        )
    return is_safe


def get_students(a_day: bytes, b_day: bytes) -> dict[str, list]:
    """Extract student data from two CSV files.

    Args:
        a_day (bytes): The A day CSV file in bytes.
        b_day (bytes): The B day CSV file in bytes.
    Returns:
        dict[str, list[list[str, int]]]: A dictionary with keys 'a' and 'b' containing student data.
    """

    a_day_students = pd.read_csv(StringIO(a_day.decode("utf-8"))).values.tolist()
    b_day_students = pd.read_csv(StringIO(b_day.decode("utf-8"))).values.tolist()

    return {"a": a_day_students, "b": b_day_students}
