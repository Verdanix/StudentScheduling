"""Helper functions for the scheduling algorithm."""

import datetime
import random
from io import StringIO
from itertools import cycle

import icalendar
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


def schedule_shifts(
    students: dict[str, list], days: list[datetime.date], min_employees: int
) -> dict[datetime.date, list[str]]:
    """Schedule shifts for students based on the provided days and constraints.

    Args:
        students (dict[str, list]): A dictionary with keys 'a' and 'b' containing student data.
        days (list[datetime.date]): List of dates to schedule shifts for.
        min_employees (int): Minimum number of employees required for each shift.
    Returns:
        dict[datetime.date, list[str]]: A dictionary mapping each date to a list of scheduled students.

    """

    def create_dictionary(shift_days: list[datetime.date], values: list):
        """Create a schedule dictionary for the given shift days and student values.

        Args:
            shift_days (list[datetime.date]): List of dates to schedule shifts for.
            values (list): List of student data to assign to shifts.
        Returns:
            dict[datetime.date, list[str]]: A dictionary mapping each date to a list of scheduled students.
        """

        schedule = {day.day: [] for day in shift_days}
        cycled_values = cycle(values)
        for day in shift_days:
            schedule[day.day] = [next(cycled_values)[0] for _ in range(min_employees)]
        return schedule

    def get_schedule(students_scheduled: list, needed_employees: int, day_offset: int):
        """Get the schedule for either A days or B days.

        Args:
            students_scheduled (list): List of student data to assign to shifts.
            needed_employees (int): Total number of employees needed for the shifts.
            day_offset (int): Offset to determine whether to schedule A days or B days.
        Returns:
            dict[datetime.date, list[str]]: A dictionary mapping each date to a list of scheduled students.
        """
        random.shuffle(students_scheduled)
        shift_days = days[day_offset:needed_employees:2]
        return create_dictionary(shift_days, students_scheduled)

    total_days_split = len(days) // 2
    total_needed_employees = (
        total_days_split * min_employees
    )  # Total employees needed for either A days or B days for the entire period

    a_day_schedule = get_schedule(students["a"], total_needed_employees, 0)
    b_day_schedule = get_schedule(students["b"], total_needed_employees, 1)
    merged_dict = {**a_day_schedule, **b_day_schedule}
    return dict(sorted(merged_dict.items()))


def create_ics_file(schedule: dict, month: int, year: int) -> bytes:
    """Create an ICS file from the schedule.

    Args:
        schedule (dict): A dictionary mapping each date to a list of scheduled students.
        month (int): The month for the schedule.
        year (int): The year for the schedule.
    Returns:
        bytes: The ICS file in bytes.
    """
    calendar = icalendar.Calendar()
    # Compress the schedule data into a list of (day, student) tuples. Little cleaner
    compressed_data = [
        (day, student) for day, students in schedule.items() for student in students
    ]
    for day, student in compressed_data:
        event = icalendar.Event()
        event.add("summary", student)
        event.add("dtstart", datetime.date(year, month, day))
        event.add("dtend", datetime.date(year, month, day))
        calendar.add_component(event)
    return calendar.to_ical()
