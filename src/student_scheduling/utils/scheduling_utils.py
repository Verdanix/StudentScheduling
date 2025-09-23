"""Helper functions for the scheduling algorithm."""

import datetime
import random
from itertools import cycle

from config.logging import logger


def create_dictionary(
    shift_days: list[datetime.date], values: list, min_employees: int
):
    """Create a schedule dictionary for the given shift days and student values.

    Args:
        shift_days (list[datetime.date]): List of dates to schedule shifts for.
        values (list): List of student data to assign to shifts.
        min_employees (int): Minimum required employees to schedule per day.
    Returns:
        dict[datetime.date, list[str]]: A dictionary mapping each date to a list of scheduled students.
    """

    schedule = {day.day: [] for day in shift_days}
    cycled_values = cycle(values)
    for day in shift_days:
        schedule[day.day] = [next(cycled_values)[0] for _ in range(min_employees)]
    return schedule


def get_schedule(
    students_scheduled: list,
    days: list[datetime.date],
    needed_employees: int,
    day_offset: int,
    min_employees: int,
):
    """Get the schedule for either A days or B days.

    Args:
        students_scheduled (list): List of student data to assign to shifts.
        days (list): List of the days to schedule for.
        needed_employees (int): Total number of employees needed for the shifts.
        day_offset (int): Offset to determine whether to schedule A days or B days.
        min_employees (int): Minimum required employees scheduled per day.
    Returns:
        dict[datetime.date, list[str]]: A dictionary mapping each date to a list of scheduled students.
    """
    random.shuffle(students_scheduled)
    shift_days = days[day_offset:needed_employees:2]
    return create_dictionary(shift_days, students_scheduled, min_employees)


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

    total_days_split = len(days) // 2

    # Total employees needed for either A days or B days for the entire period
    total_needed_employees = total_days_split * min_employees

    logger.debug("schedule_shifts: Total employees needed: %d", total_needed_employees)
    a_day_schedule = get_schedule(
        students["a"], days, total_needed_employees, 0, min_employees
    )
    b_day_schedule = get_schedule(
        students["b"], days, total_needed_employees, 1, min_employees
    )

    merged_dict = {**a_day_schedule, **b_day_schedule}
    return dict(sorted(merged_dict.items()))
