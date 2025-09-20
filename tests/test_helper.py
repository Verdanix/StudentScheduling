import datetime
from pathlib import Path

import pytest

from src.student_scheduling.helper import filter_weekends, get_days, filter_days, filter_excluded_dates, csv_has_csv_mime_type, csv_has_2_columns, get_students, schedule_shifts
from student_scheduling.models import Submission

ranges = {
    1: [datetime.date(2025, 9, 1), datetime.date(2025, 9, 30)],
    2: [datetime.date(2025, 10, 1), datetime.date(2025, 10, 31)],
    3: [datetime.date(2025, 11, 1), datetime.date(2025, 11, 30)],
}

csv = {
    "bad": Path("tests/files/bad.csv").read_bytes(),
    "good": Path("tests/files/good.csv").read_bytes(),
    "a": Path("tests/files/a_day.csv").read_bytes(),
    "b": Path("tests/files/b_day.csv").read_bytes(),
}


def test_get_days_content():
    """Test get_days for all predefined ranges."""
    for range_id, (start_day, end_day) in ranges.items():
        days = get_days(start_day, end_day)
        for i, day in enumerate(days):
            print("Range ID:", range_id, "Day:", day)
            assert day == start_day + datetime.timedelta(days=i)


def test_get_days_length():
    """Test get_days for all predefined ranges."""
    for range_id, (start_day, end_day) in ranges.items():
        days = get_days(start_day, end_day)
        print("Range ID:", range_id, "Days Length:", len(days))
        assert len(days) == (end_day - start_day).days + 1


def test_filter_weekends():
    for range_id, (start_day, end_day) in ranges.items():
        days = get_days(start_day, end_day)
        weekdays = filter_weekends(days)
        print("Range ID:", range_id, "Weekdays Length:", len(weekdays))
        assert all(day.weekday() < 5 for day in weekdays)


def test_filter_excluded_dates():
    for range_id, (start_day, end_day) in ranges.items():
        month = start_day.month

        excluded_dates = [
            datetime.date(2025, month, 5),
            datetime.date(2025, month, 10),
            datetime.date(2025, month, 15),
        ]

        days = get_days(start_day, end_day)
        days = filter_excluded_dates(days, excluded_dates)
        print("Range ID:", range_id, "Filtered Days Length:", len(days))
        assert all(day not in excluded_dates for day in days)


def test_filter_days():
    for range_id, (start_day, end_day) in ranges.items():
        month = start_day.month

        excluded_dates = [
            datetime.date(2025, month, 5),
            datetime.date(2025, month, 10),
            datetime.date(2025, month, 15),
        ]

        days = get_days(start_day, end_day)
        days = filter_days(days, excluded_dates)
        print("Range ID:", range_id, "Filtered Days Length:", len(days))
        assert all(day not in excluded_dates for day in days)
        assert all(day.weekday() < 5 for day in days)


def test_is_safe_csv():
    assert csv_has_csv_mime_type(csv["good"])
    assert csv_has_csv_mime_type(csv["bad"])


def test_has_2_columns_exactly():
    assert csv_has_2_columns(csv["good"])
    assert not csv_has_2_columns(csv["bad"])


def test_safe_csv():
    assert csv_has_csv_mime_type(csv["good"])
    assert csv_has_csv_mime_type(csv["bad"])


def test_validate_csv():
    assert Submission.validate_csv(csv['good'], csv['good']) is None
    with pytest.raises(ValueError) as info:
        Submission.validate_csv(csv['good'], csv['bad'])


def test_is_valid_data_structure():
    students = get_students(csv['good'], csv['good'])
    assert len(students.keys()) == 2
    assert type(students) is dict
    assert type(students['a']) is list
    assert type(students['b']) is list


def test_scheduling_output_datatype():
    students = get_students(csv['a'], csv['b'])
    min_daily_employees = 5
    for start, end in ranges.values():
        days = get_days(start, end)
        days = filter_days(days, [])
        schedule = schedule_shifts(students, days, min_daily_employees)
        assert type(schedule) is dict
