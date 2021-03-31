"""This module generates random candidates data to be saved in csv/excel file"""
import random
from datetime import datetime
from faker import Faker
from pesel import Pesel

HIGHSCHOOL_TYPE = ["Liceum", "Technikum"]
FACULTIES = ["WIET", "WEAIB", "WIMIC", "WIMIR", "WZ", "WIMIP"]
DEGREE = ["BACHELOR", "MASTER"]
MAJORS = open("field_of_studies").read().splitlines()
MODE = ["PART-TIME", "FULL-TIME"]
faker = Faker('pl_PL')


class CandidateData():
    """Stores candidate data"""
    def __init__(self, recruitment_data):
        self.recruitment_data = recruitment_data
        self.pesel = Pesel.generate()
        self.name = faker.name()
        self.city = faker.city()
        self.region = faker.region()
        self.country = "Polska"
        self.highschool = random.choice(HIGHSCHOOL_TYPE) + " nr " + str(random.randrange(10) + 1)
        self.highschool_city = faker.city()
        self.matura_date = faker.date_between_dates(date_start=datetime(2017,1,1),
                                                date_end=recruitment_data.end_date)
        self.matura_result = random.randrange(100)
        if recruitment_data.degree == "MASTER":
            self.graduation_date = faker.date_between_dates(date_start=self.matura_date,
                                        date_end=recruitment_data.end_date)
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
        candidate = cls.__new__(cls)
        candidate.recruitment_data = recruitment_data
        candidate.pesel = other.pesel
        candidate.name = other.name
        candidate.city = other.city
        candidate.region = other.region
        candidate.country = other.country
        candidate.highschool = other.highschool
        candidate.highschool_city = other.highschool_city
        candidate.matura_date = other.matura_date
        candidate.matura_result = other.matura_result
        if recruitment_data.degree == "MASTER" and other.recruitment_data.degree == 'BACHELOR':
            candidate.graduation_date = faker.date_between_dates(
                                        date_start=other.recruitment_data.end_date,
                                        date_end=recruitment_data.end_date)
            candidate.college_name = "AGH University"
            candidate.faculty = other.recruitment_data.faculty
            candidate.field_of_study = other.recruitment_data.major_name
            candidate.mode = other.recruitment_data.mode
            candidate.average = random.uniform(2.0, 5.0)
        else:
            candidate.graduation_date = other.graduation_date
            candidate.college_name = other.college_name
            candidate.faculty = other.faculty
            candidate.field_of_study = other.field_of_study
            candidate.mode = other.mode
            candidate.average = other.average
        return candidate

    def can_be_next_recruitment(self, recruitment):
        if recruitment.end_date < self.recruitment_data.end_date:
            return False
        return True

    def __iter__(self):
        return iter([self.pesel, self.name, self.city, self.region, self.country, self.highschool,
                    self.highschool_city, self.matura_date, self.graduation_date,self.matura_result,
                    self.college_name, self.faculty, self.field_of_study, self.mode, self.average]
                    + list(self.recruitment_data))
