from src.student_scheduling.utils.csv_utils import csv_has_csv_mime_type, csv_has_2_columns, get_students
from tests.unit.data import csv
from src.student_scheduling.models import Submission
import pytest

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
