"""Helper functions for the scheduling algorithm."""

import datetime


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
