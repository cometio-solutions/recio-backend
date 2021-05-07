"""This module contains endpoint for getting recruitment points of candidates"""
import logging
import sys

from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, request
from rest.common.token import handle_request_token
from rest.common.response import create_response, options_response
from rest.models.candidate_recruitment import CandidateRecruitment
from rest.models.recruitment import Recruitment


points_sum_url = Blueprint('points', __name__)


@points_sum_url.before_request
def handle_options():
    """
    Handles OPTIONS method before recruitment endpoint
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    return options_response(request)


@points_sum_url.route('/<recruitment_id>', methods=['GET', 'OPTIONS'])
def get_points_sum(recruitment_id):
    """
    Gets the number of candidates that have gotten certain number of points.

    Returns list of dictionaries containing 'points' and 'numberOfStudents':
    [
        {
            'points': <integer>
            'numberOfStudents': <integer>
        }
        ...
    ]
    :param recruitment_id: id of recruitment
    :return: flask Response containing json with points sum
    """

    logging.info("Getting recruitment points sum")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is None!")
        return response

    points = {}

    try:
        if not Recruitment.query.filter_by(id=recruitment_id).first():
            logging.warning('Nie znaleziono rekrutacji o takim ID')
            return create_response({'error': 'Nie znaleziono podanej rekrutacji ID'}, 404, '*')

        for rec in CandidateRecruitment.query.filter_by(recruitment_id=recruitment_id):
            if rec.points not in points:
                points[rec.points] = 1
            else:
                points[rec.points] += 1

    except (AttributeError, SQLAlchemyError) as exception:
        logging.error(exception, file=sys.stderr)
        return create_response({'error': 'Błąd podczas pobierania punktów'}, 400, '*')

    points_sum = [{'points': key, 'numberOfStudents': value} for key, value in points.items()]

    return create_response(points_sum, 200, '*')
