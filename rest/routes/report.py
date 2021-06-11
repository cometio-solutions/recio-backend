"""This module is for endpoints about PDF reports"""

import logging
from flask import Blueprint, request, send_from_directory
from sqlalchemy.exc import SQLAlchemyError
from rest.common.response import create_response, options_response
from rest.common.token import handle_request_token
from rest.common.report import generate_recruitment_year_report
from rest.models.recruitment import Recruitment
from rest.generators.recruitment import generate_plots


report_url = Blueprint('report', __name__)


@report_url.route('/<year>', methods=['GET', 'OPTIONS'])
def get_recruitment_pdf_for_year(year):
    """
    Endpoint for getting reports for recruitments from certain year.

    :param year: year of the recruitments to get
    :return: pdf file if success else response with error message
    """
    if request.method == 'OPTIONS':
        return options_response(request)

    role, response = handle_request_token(request)

    if role is None:
        logging.warning('Role is None!')
        return response

    try:
        path = generate_recruitment_year_report(year)
    except Exception as ex:
        logging.error(ex)
        return create_response({'error': 'Błąd podczas tworzenia PDFu'}, 400, '*')

    if path == 404:
        return create_response({'error': 'Nie znaleziono rekrutacji dla podanego roku'}, 404, '*')

    response = send_from_directory(
        directory='.',
        path='/',
        filename=path,
        mimetype='application/pdf',
        as_attachment=True,
    )

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['content-disposition'] = 'attachment; filename = ' + path
    return response


@report_url.route('/plots', methods=['GET', 'OPTIONS'])
def get_plots_recruitments_pdf_report():
    if request.method == 'OPTIONS':
        return options_response(request)

    role, response = handle_request_token(request)

    if role is None:
        logging.warning('Role is None!')
        return response

    try:
        all_recruitments = Recruitment.query.all()
    except SQLAlchemyError:
        return create_response({'error': 'Błąd w trakcie pobierania danych'}, 400, '*')\

    recruitments = []
    for rec in all_recruitments:
        summary = Recruitment.get_cycles_summary([rec])
        rec_json = Recruitment.to_json(rec, summary['overall_candidates_num'])

        if rec_json['point_limit'] is None:
            rec_json['point_limit'] = 0

        recruitments.append(rec_json)

    try:
        path = generate_plots(recruitments)
    except Exception as ex:
        logging.error(ex)
        return create_response({'error': 'Błąd podczas tworzenia PDFu'}, 400, '*')

    response = send_from_directory(
        directory='.',
        path='/',
        filename=path,
        mimetype='application/pdf',
        as_attachment=True,
    )

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['content-disposition'] = 'attachment; filename = ' + path
    return response
