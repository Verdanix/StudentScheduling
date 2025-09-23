"""Helper functions for the ICS generation."""

import datetime

import icalendar


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
