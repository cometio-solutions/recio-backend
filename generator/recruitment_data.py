"""This module generates random recruitment data to be saved in csv/excel file"""
import random
import copy
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
        recruitment = copy.deepcopy(other)
        recruitment.end_date = faker.date_between_dates(date_start=other.end_date,
                                                        date_end=datetime(2021, 12, 31))
        recruitment.cycle_number = other.cycle_number + 1
        recruitment.slot_limit = random.randrange(int(other.slot_limit/2)) + 10
        return recruitment

    def get_dict(self):
        """
        Creates dict that is useful for writing Recruitment data to csv/excel files
        :return: dict of Recruitment data objects
        """
        values = copy.deepcopy(self.__dict__)
        values['end_date'] = str(self.end_date)
        return values
