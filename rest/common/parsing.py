"""Module for parsing .csv and .xlsx files"""
import csv
import pylightxl as xl


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
        recruitment_end_date, recruitment_cycle_number, recruitment_slot_limit

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
    if columns_number == 23:
        return 'C'
    elif columns_number == 7:
        return 'R'
    else:
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
    for i, c in enumerate(row):
        if columns[i] == 'name' and c.split(' ')[0] in ['pan', 'pani']:
            c = c[c.find(' ') + 1:]

        if isinstance(c, str) and len(c) == 0:
            single[columns[i]] = None
        else:
            single[columns[i]] = c

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

    for ws in excel_file.ws_names:
        document_type = check_document_type(len(excel_file.ws(ws=ws).row(row=1)))
        columns = excel_file.ws(ws=ws).row(row=1)
        file_data = []

        for i, row in enumerate(excel_file.ws(ws=ws).rows):
            if i != 0:
                file_data.append(handle_row(row, columns))

        data.append((document_type, file_data))

    return data
