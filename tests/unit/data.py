import datetime
from pathlib import Path
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