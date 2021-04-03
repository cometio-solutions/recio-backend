"""This module generates random candidates data to be saved in csv/excel file"""
import random
import copy
from datetime import datetime
from utils import HIGHSCHOOL_TYPE, FACULTIES, MAJORS, MODE, faker
from pesel import Pesel


class CandidateData():
    """Stores candidate data"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, recruitment_data):
        self.recruitment_data = recruitment_data
        self.pesel = str(Pesel.generate())
        self.name = faker.name()
        self.city = faker.city()
        self.region = faker.region()
        self.country = "Polska"
        self.highschool = random.choice(HIGHSCHOOL_TYPE) + " nr " + str(random.randrange(10) + 1)
        self.highschool_city = faker.city()
        self.matura_date = faker.date_between_dates(date_start=datetime(2017, 1, 1),
                                                    date_end=recruitment_data.end_date)
        self.matura_result = random.randrange(100)
        self.test_result = random.randrange(100)
        if recruitment_data.degree == "MASTER":
            self.graduation_date = str(faker.date_between_dates(date_start=self.matura_date,
                                                                date_end=recruitment_data.end_date))
            self.college_name = "University of " + faker.word()
            self.faculty = random.choice(FACULTIES)
            self.field_of_study = random.choice(MAJORS)
            self.mode = random.choice(MODE)
            self.average = random.uniform(2.0, 5.0)
        else:
            self.graduation_date = None
            self.college_name = None
            self.faculty = None
            self.field_of_study = None
            self.mode = None
            self.average = None

    @classmethod
    def from_previous_recruitment(cls, other, recruitment_data):
        """
        Creates candidate data (next recruitment) from other candidate data
        :param other: Candidate data for previous recruitment
        :return: Candidate data for next recruitment
        """
        candidate = copy.deepcopy(other)
        candidate.recruitment_data = recruitment_data
        candidate.test_result = random.randrange(100)
        if recruitment_data.degree == "MASTER" and other.recruitment_data.degree == 'BACHELOR':
            candidate.graduation_date = str(faker.date_between_dates(
                                        date_start=other.recruitment_data.end_date,
                                        date_end=recruitment_data.end_date))
            candidate.college_name = "AGH University"
            candidate.faculty = other.recruitment_data.faculty
            candidate.field_of_study = other.recruitment_data.major_name
            candidate.mode = other.recruitment_data.mode
            candidate.average = random.uniform(2.0, 5.0)
        return candidate

    def can_be_next_recruitment(self, recruitment):
        """
        Checks if candidate can take part in the next recruitment
        :param recruitment: Possible next recruitment
        :return: True if candidate can take part in the recruitment, False otherwise
        """
        if recruitment.end_date < self.recruitment_data.end_date:
            return False
        if recruitment.degree == "BACHELOR" and self.recruitment_data.degree == "MASTER":
            return False
        return True

    def get_dict(self):
        """
        Creates dict that is useful for writing Candidate data to csv/excel files
        :return: dict of Candidate data objects
        """
        values = copy.deepcopy(self.__dict__)
        values['matura_date'] = str(self.matura_date)
        values.pop('recruitment_data')
        recruitment_values = {"recruitment_" + str(key): val for key, val in
                              self.recruitment_data.get_dict().items()}
        return {**values, **recruitment_values}
