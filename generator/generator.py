"""This modules generates and saves data in csv/excel file"""
import csv
import random
import sys
import xlsxwriter
from recruitment_data import RecruitmentData
from candidate_data import CandidateData


def generate_data(recruitments_number, cycle_number):
    """
    Generates recruitment and candidates data
    :param recruitments_number: Number of recruitments you want to generate
    :return: List of generated RecruitmentData and CandidateData
    """
    recruitments = [RecruitmentData() for _ in range(recruitments_number)]
    for recruitment in list(recruitments):
        for _ in range(cycle_number):
            recruitment = RecruitmentData.from_previous_cycle(recruitment)
            recruitments.append(recruitment)
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
        writer.writerow(list(recruitments[0].get_dict().keys()))
        for recruitment in recruitments:
            writer.writerow(list(recruitment.get_dict().values()))
    with open("candidates.csv", 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(list(candidates[0].get_dict().keys()))
        for candidate in candidates:
            writer.writerow(list(candidate.get_dict().values()))


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
    column_names = list(recruitments[0].get_dict().keys())
    for name in column_names:
        worksheet.write(row, column, name)
        column += 1
    for recruitment in recruitments:
        row += 1
        column = 0
        for data in list(recruitment.get_dict().values()):
            worksheet.write(row, column, data)
            column += 1
    worksheet = workbook.add_worksheet("Candidates")
    row = 0
    column = 0
    column_names = list(candidates[0].get_dict().keys())
    for name in column_names:
        worksheet.write(row, column, name)
        column += 1
    for candidate in candidates:
        row += 1
        column = 0
        for data in list(candidate.get_dict().values()):
            worksheet.write(row, column, data)
            column += 1
    workbook.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 generator.py <number of recruitments to generate> <number of cycles>")
    if int(sys.argv[1]) == 0:
        print("You need to generete at least one recruitment")
    else:
        recruitment_number = int(sys.argv[1])
        recruitments_data, candidates_data = generate_data(recruitment_number, int(sys.argv[2]))
        generate_csv(recruitments_data, candidates_data)
        generate_excel(recruitments_data, candidates_data)
