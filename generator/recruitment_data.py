"""This module generates random recruitment data to be saved in csv/excel file"""
import random
from datetime import datetime
from utils import DEGREE, FACULTIES, MAJORS, MODE, faker


class RecruitmentData():
    """Stores recruitment data"""
    def __init__(self):
        self.faculty = random.choice(FACULTIES)
        self.degree = random.choice(DEGREE)
        self.major_name = random.choice(MAJORS)
        self.mode = random.choice(MODE)
        self.end_date = faker.date_between_dates(date_start=datetime(2018, 1, 1),
                                                 date_end=datetime(2021, 12, 31))
        self.cycle_number = 1
        self.slot_limit = random.randrange(200) + 10

    @classmethod
    def from_previous_cycle(cls, other):
        """
        Creates recruitment data (next cycle) from other recruitment data
        :param other: Recruitment data for previous recruitment cycle
        :return: Recruitment data for next recruitment cycle
        """
        recruitment = cls.__new__(cls)
        recruitment.faculty = other.faculty
        recruitment.degree = other.degree
        recruitment.major_name = other.major_name
        recruitment.mode = other.mode
        recruitment.end_date = faker.date_between_dates(date_start=other.end_date,
                                                        date_end=datetime(2021, 12, 31))
        recruitment.cycle_number = other.cycle_number + 1
        recruitment.slot_limit = random.randrange(int(other.slot_limit/2)) + 10
        return recruitment

    def __iter__(self):
        return iter([self.faculty, self.degree, self.major_name, self.mode,
                    str(self.end_date), self.cycle_number, self.slot_limit])
