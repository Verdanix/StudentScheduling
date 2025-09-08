"""Helper functions for the scheduling algorithm."""

import datetime
from io import StringIO

import magic
import pandas as pd


def filter_weekends(dates: list[datetime.date]) -> list[datetime.date]:
    """Filter out weekends from a list of dates.

    Args:
        dates (list[datetime.date]): List of dates to filter.
    Returns:
        list[datetime.date]: Filtered list of dates excluding weekends.
    """
    return [
        date for date in dates if date.weekday() < 5
    ]  # 0-4 are weekdays, 5-6 are weekends


def filter_excluded_dates(
    dates: list[datetime.date], excluded_dates: list[datetime.date]
) -> list[datetime.date]:
    """Filter out excluded dates from a list of dates.

    Args:
        dates (list[datetime.date]): List of dates to filter.
        excluded_dates (list[datetime.date]): List of dates to exclude.
    Returns:
        list[datetime.date]: Filtered list of dates.
    """
    return [date for date in dates if date not in excluded_dates]


def filter_days(
    dates: list[datetime.date], excluded_dates: list[datetime.date]
) -> list[datetime.date]:
    """Filter out weekends and excluded dates from a list of dates.

    Args:
        dates (list[datetime.date]): List of dates to filter.
        excluded_dates (list[datetime.date]): List of dates to exclude.
    Returns:
        list[datetime.date]: Filtered list of dates.
    """
    dates = filter_weekends(dates)
    dates = filter_excluded_dates(dates, excluded_dates)
    return dates


def get_days(start_day: datetime.date, end_day: datetime.date) -> list[datetime.date]:
    """
    Generate a list of dates between start_day and end_day, inclusive.

    Args:
        start_day (datetime.date): The starting date.
        end_day (datetime.date): The ending date.

    Returns:
        list[datetime.date]: A list of dates from start_day to end_day.
    """
    delta = end_day - start_day
    return [start_day + datetime.timedelta(days=i) for i in range(delta.days + 1)]


def csv_has_csv_mime_type(content: bytes) -> bool:
    """Check if the uploaded file is a safe CSV file. This is the first layer of safety

    Args:
        content (bytes): The file to check in bytes.
    Returns:
        bool: True if the file is a safe CSV file, False otherwise.
    """

    max_file_size = 15 * 1024 * 1024  # 15 MB

    if len(content) > max_file_size:
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
        print(df.shape[1])
        return df.shape[1] == 2
    except Exception:
        return False


def csv_is_safe(content: bytes) -> bool:
    """Check if the uploaded CSV file is safe by verifying its MIME type and column count.

    Args:
        content (bytes): The CSV file to check.
    Returns:
        bool: True if the file is safe, False otherwise.
    """
    return csv_has_csv_mime_type(content) and csv_has_2_columns(content)
