import datetime
from pathlib import Path

import pytest

from src.student_scheduling.utils.date_utils import filter_days, get_days
from src.student_scheduling.utils.csv_utils import get_students
from src.student_scheduling.helper import schedule_shifts
from student_scheduling.models import Submission

from tests.unit.data import ranges, csv


def test_scheduling_output_datatype():
    students = get_students(csv['a'], csv['b'])
    min_daily_employees = 5
    for start, end in ranges.values():
        days = get_days(start, end)
        days = filter_days(days, [])
        schedule = schedule_shifts(students, days, min_daily_employees)
        assert type(schedule) is dict
