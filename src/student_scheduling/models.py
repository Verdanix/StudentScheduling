"""The models module contains data models for handling submissions and configurations"""

import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class HallPass(BaseModel):
    """
    Represents a hall pass configuration for shifts in the student-run store.

    Attributes:
        checked (bool):
            Indicates whether the hall pass output is toggled.
            Defaults to False.

        signature_required (bool):
            Indicates whether a signature is required on the hall pass.
            This is a mandatory field and must be provided when creating a HallPass instance.
    """

    checked: bool = False
    signature_required: bool


class Submission(BaseModel):
    """
    Represents a submission for scheduling shifts in the student-run store.

    Attributes:
        a_day (UploadFile):
            The file containing the schedule for A-day students.
            This file is expected to be uploaded by the user and should follow a predefined format.

        b_day (UploadFile):
            The file containing the schedule for B-day students.
            Similar to `a_day`, this file should adhere to the same format.

        start_date (datetime.date):
            The starting date for the scheduling period.
            All shifts will be generated starting from this date.

        end_date (datetime.date):
            The ending date for the scheduling period.
            No shifts will be scheduled beyond this date.

        excluded_dates (list[datetime.date]):
            A list of specific dates to exclude from the schedule.
            These dates can represent holidays, special events, or any other days when the store will not operate.
            Defaults to an empty list.

        min_employees (int):
            The minimum number of employees required for each shift.
            This ensures that the store is adequately staffed.
            Defaults to 5.

        min_monthly_employee_shifts (int):
            The minimum number of shifts each employee must work per month.
            This helps distribute the workload evenly among employees.
            Defaults to 2.

        ics (bool):
            A flag indicating whether the generated schedule should be exported in the iCal format.
            If `True`, an iCal file will be created for easy import into calendar applications.
            Defaults to `True`.

        store_name (str):
            The name of the store for which the schedule is being generated.
            This is used for identification and labeling purposes.

        hall_pass (HallPass):
            An object representing the hall pass configuration for the shifts.
            Includes options such as whether a signature is required on the hall pass.
            Defaults to a `HallPass` object with `signature_required` set to `False`.
    """

    a_day: UploadFile
    b_day: UploadFile
    start_date: datetime.date
    end_date: datetime.date
    excluded_dates: list[datetime.date] = []
    min_employees: int = 5
    min_monthly_employee_shifts: int = 2
    ics: bool = True
    store_name: str
    hall_pass: HallPass = HallPass(signature_required=False)
