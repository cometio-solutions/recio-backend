"""Utils for candidate data and recruitment data"""
from faker import Faker

HIGHSCHOOL_TYPE = ["Liceum", "Technikum"]
FACULTIES = ["WIET", "WEAIB", "WIMIC", "WIMIR", "WZ", "WIMIP"]
DEGREE = ["BACHELOR", "MASTER"]
MAJORS = open("field_of_studies").read().splitlines()
MODE = ["PART-TIME", "FULL-TIME"]
faker = Faker('pl_PL')
