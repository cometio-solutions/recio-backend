"""This module contains endpoint about getting years of recruitments"""
import logging
from flask import Blueprint, request
from rest.models.recruitment import Recruitment
from rest.common.response import create_response
from rest.common.token import handle_request_token


years_url = Blueprint('years', __name__)


@years_url.route('', methods=['GET', 'OPTIONS'])
def get_years():
    """
    Gets all years in which Recruitment happened.
    :return: flask response object with a list of years
    """
    if request.method == 'OPTIONS':
        logging.info("Handle options")
        return create_response({}, 200, '*', 'content-type, token')

    logging.info("Getting recruitment years")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is None!")
        return response

    years = set()
    for rec in Recruitment.query.all():
        if rec.end_date.year not in years:
            years.add(rec.end_date.year)

    years = list(years)
    years.sort(reverse=True)

    return create_response(years, 200, '*')
