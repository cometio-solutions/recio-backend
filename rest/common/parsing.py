"""Module for parsing .csv and .xlsx files"""
import csv
import pylightxl as xl
from rest.db import db
from rest.models.major import Major
from rest.models.recruitment import Recruitment
from rest.models.candidate import Candidate
from rest.models.candidate_recruitment import CandidateRecruitment


def parse_file(file):
    """
    This function should be used to parse files.
    Accepts only .csv and .xlsx files.

    There are two document types: 'C' and 'R'.

    If a field in document was empty there is None type in dictionary.

    The following are fields in the dictionary for 'C' (candidate) file type (23 total):
        pesel, name, city,region, country, highschool, highschool_city, matura_date, matura_result,
        test_result, graduation_date, college_name, faculty, field_of_study, mode,average,
        recruitment_faculty, recruitment_degree, recruitment_major_name, recruitment_mode,
        recruitment_end_date, recruitment_cycle_number, recruitment_slot_limit, is_paid

    The following are fields in the dictionary for 'R' (recruitments) file type (7 total):
        faculty, degree, major_name, mode, end_date, cycle_number, slot_limit

    :param file: file to be parsed
    :return: list of pairs (document type, list of dictionaries),
        where in each of the dictionary there is one candidate/recruitment
    """
    if file.endswith('.csv'):
        return parse_csv(file)

    if file.endswith('.xlsx'):
        return parse_excel(file)

    raise ValueError("We only support .csv and .xlsx files!")


def check_document_type(columns_number):
    """
    Common function for all types of files.
    Checks whether the document has candidates or recruitments.
    Raises error if there is bad number of columns.
    :param columns_number: Number of columns (length of the row)
    :return: String, either 'C' (candidates) or 'R' (recruitments)
    """
    if columns_number == 24:
        return 'C'

    if columns_number == 7:
        return 'R'

    raise ValueError("Import file must have 23 columns for candidates"
                     "or 7 columns for recruitments!")


def handle_row(row, columns):
    """
    Common function for all types of files.
    Handles one row of normal input.
    :param row: Data of one candidate/recruitment
    :param columns: List of column names
    :return: Dictionary with the candidate/recruitment data
    """
    single = {}
    for i, val in enumerate(row):
        if columns[i] == 'name' and val.split(' ')[0] in ['pan', 'pani']:
            val = val[val.find(' ') + 1:]

        if isinstance(val, str) and len(val) == 0:
            single[columns[i]] = None
        else:
            single[columns[i]] = val

    return single


def parse_csv(file):
    """
    Parser of .csv files.
    :param file: .csv file to be parsed
    :return: list of pairs (document type, list of dictionaries),
        where in each of the dictionary there is one candidate/recruitment
    """
    data = []
    document_type = None
    columns = []

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                document_type = check_document_type(len(row))
                columns = row
            else:
                data.append(handle_row(row, columns))

    return [(document_type, data)]


def parse_excel(file):
    """
    Parser of .xlsx files.
    :param file: .xlsx file to be parsed
    :return: list of pairs (document type, list of dictionaries),
        where in each of the dictionary there is one candidate/recruitment
    """
    data = []
    excel_file = xl.readxl(file)

    for worksheet in excel_file.ws_names:
        document_type = check_document_type(len(excel_file.ws(ws=worksheet).row(row=1)))
        columns = excel_file.ws(ws=worksheet).row(row=1)
        file_data = []

        for i, row in enumerate(excel_file.ws(ws=worksheet).rows):
            if i != 0:
                file_data.append(handle_row(row, columns))

        data.append((document_type, file_data))

    return data


def save_data(data):
    """
    Saves data in database
    :param data: list of pairs (document type, list of dictionaries),
        where in each of the dictionary there is one candidate/recruitment
    """
    for pair in data:
        doc_type, doc_data = pair
        if doc_type == 'R':
            for recruitment in doc_data:
                save_recruitment(recruitment)
        else:
            save_candidates(doc_data)


def save_recruitment(rec_dict):
    """
    Saves recruitment and major in database if they don't exist already
    :param rec_dict: dictionary with recruitment data
    :return: Recruitment
    """
    major = Major.query.filter_by(name=rec_dict['major_name'], faculty=rec_dict['faculty'],
                                  degree=rec_dict['degree'], mode=rec_dict['mode']).first()
    if not major:
        major = Major.from_dict(rec_dict)
        db.session.add(major)
        db.session.commit()
    recruitment = Recruitment.query.filter_by(major_id=major.id,
                                              cycle_number=rec_dict['cycle_number'],
                                              end_date=rec_dict['end_date']).first()
    if not recruitment:
        recruitment = Recruitment.from_dict(rec_dict)
        if recruitment.cycle_number != 1:
            previous_recruitment = Recruitment.query\
                                              .filter_by(major_id=major.id,
                                                         cycle_number=(recruitment.cycle_number-1))\
                                              .filter(Recruitment.end_date < recruitment.end_date)\
                                              .first()
            recruitment.previous_recruitment = previous_recruitment
        recruitment.major = major
        db.session.add(recruitment)
    db.session.commit()
    return recruitment


def save_candidates(candidates):
    """
    Saves candidates in database
    :param candidates: List of dictionaries where in each of dictionary is one candidate
    """
    for can_dict in candidates:
        rec_dict = {key.replace('recruitment_', ''): value
                    for key, value in can_dict.items() if key.startswith('recruitment')}
        recruitment = save_recruitment(rec_dict)
        candidate = Candidate.query.filter_by(pesel=int(can_dict['pesel'])).first()
        if not candidate:
            candidate = Candidate.from_dict(can_dict)
            db.session.add(candidate)
            db.session.commit()
        candidate_recruitment = CandidateRecruitment.from_dict(can_dict)
        candidate_recruitment.candidate = candidate
        candidate_recruitment.recruitment = recruitment
        db.session.add(candidate_recruitment)
        db.session.commit()
