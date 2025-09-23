"""Utilities for processing dates."""

import datetime
from config.logging import logger


def filter_weekends(dates: list[datetime.date]) -> list[datetime.date]:
    """Filter out weekends from a list of dates.

    Args:
        dates (list[datetime.date]): List of dates to filter.
    Returns:
        list[datetime.date]: Filtered list of dates excluding weekends.
    """
    logger.debug("filter_weekends: Starting with %d dates.", len(dates))
    logger.debug(
        "filter_weekends: Input dates: %r%s", dates[:5], "..." if len(dates) > 5 else ""
    )

    filtered_dates = [date for date in dates if date.weekday() < 5]
    logger.info(
        "filter_weekends: Filtered %d weekends. Remaining: %d",
        len(dates) - len(filtered_dates),
        len(filtered_dates),
    )
    return filtered_dates


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
    logger.debug("filter_excluded_dates: Filtering excluded dates: %r", excluded_dates)
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
    logger.info(
        "filter_days: Filtered the weekends and removed any dates to be excluded."
    )
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
    logger.debug(
        "get_days: Generating dates from %s to %s. Total days: %d",
        start_day,
        end_day,
        delta.days + 1,
    )
    days = [start_day + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    logger.debug(
        "get_days: Generated %d days. Sample: %r%s",
        len(days),
        days[:5],
        "..." if len(days) > 5 else "",
    )
    return days
