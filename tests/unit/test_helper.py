import datetime
from pathlib import Path

import pytest

from src.student_scheduling.utils.date_utils import filter_days, get_days
from src.student_scheduling.helper import csv_has_csv_mime_type, csv_has_2_columns, get_students, schedule_shifts
from student_scheduling.models import Submission

from tests.unit.data import ranges, csv

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
