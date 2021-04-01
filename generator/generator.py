"""This modules generates and saves data in csv/excel file"""
import csv
import random
import sys
import xlsxwriter
from recruitment_data import RecruitmentData
from candidate_data import CandidateData


def generate_data(recruitments_number):
    """
    Generates recruitment and candidates data
    :param recruitments_number: Number of recruitments you want to generate
    :return: List of generated RecruitmentData and CandidateData
    """
    recruitments = [RecruitmentData() for _ in range(recruitments_number)]
    for recruitment in list(recruitments):
        recruitments.append(RecruitmentData.from_previous_cycle(recruitment))
    candidates = [CandidateData(data) for data in recruitments]
    for recruitment in recruitments:
        number_of_candidates = random.randrange(200)
        for _ in range(number_of_candidates):
            candidate = random.choice(candidates)
            if candidate.can_be_next_recruitment(recruitment):
                candidates.append(CandidateData.from_previous_recruitment(candidate, recruitment))
            else:
                candidates.append(CandidateData(recruitment))
    return recruitments, candidates


def generate_csv(recruitments, candidates):
    """
    Generates csv file and saves data in it
    :param recruitments: List of RecruitmentData
    :param candidates: List of CandidateData
    """
    with open("recruitments.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["faculty", "degree", "major_name", "mode",
                        "end_date", "cycle_number", "slot_limit"])
        for recruitment in recruitments:
            writer.writerow(list(recruitment))
    with open("candidates.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["pesel", "name", "city", "region", "country", "highschool",
                         "highschool_city", "matura_date", "graduation_date", "matura_result",
                         "test_result", "finished_college_name", "finished_faculty",
                         "finished_field_of_study", "finished_mode", "average", "faculty",
                         "degree", "major_name", "mode", "end_date", "cycle_number", "slot_limit"])
        for candidate in candidates:
            writer.writerow(list(candidate))


def generate_excel(recruitments, candidates):
    """
    Generates excel file and saves data in it
    :param recruitments: List of RecruitmentData
    :param candidates: List of CandidateData
    """
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet("Recruitments")
    row = 0
    column = 0
    column_names = ["faculty", "degree", "major_name", "mode",
                    "end_date", "cycle_number", "slot_limit"]
    for name in column_names:
        worksheet.write(row, column, name)
        column += 1
    for recruitment in recruitments:
        row += 1
        column = 0
        for data in list(recruitment):
            worksheet.write(row, column, data)
            column += 1
    worksheet = workbook.add_worksheet("Candidates")
    row = 0
    column = 0
    column_names = ["pesel", "name", "city", "region", "country", "highschool",
                    "highschool_city", "matura_date", "graduation_date", "matura_result",
                    "test_result", "finished_college_name", "finished_faculty",
                    "finished_field_of_study", "finished_mode", "average", "faculty",
                    "degree", "major_name", "mode", "end_date", "cycle_number", "slot_limit"]
    for name in column_names:
        worksheet.write(row, column, name)
        column += 1
    for candidate in candidates:
        row += 1
        column = 0
        for data in list(candidate):
            worksheet.write(row, column, data)
            column += 1
    workbook.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 generator.py <number of recruitments to generate>")
    else:
        recruitment_number = int(sys.argv[1])
        recruitments_data, candidates_data = generate_data(recruitment_number)
        generate_csv(recruitments_data, candidates_data)
        generate_excel(recruitments_data, candidates_data)
