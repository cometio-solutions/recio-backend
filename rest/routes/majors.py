"""This module contains endpoints connected to getting data used for filtering"""
import logging
from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.major import Major


majors_url = Blueprint('majors', __name__)


@majors_url.route('', methods=['GET', 'OPTIONS'])
def get_majors():
    """
    Collects all majors present in the database.
    In JSON format:
    [
        {
            'id'
            'faculty'
            'degree'
            'name'
            'mode'
        }
        ...
    ]
    :return: flask Response containing json with all majors
    """
    if request.method == 'OPTIONS':
        logging.info("Handling options")
        return create_response({}, 200, '*', 'content-type, token')

    logging.info("Getting all majors")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is None!")
        return response

    majors = []
    for major in Major.query.all():
        majors.append({'id': major.id, 'faculty': major.faculty, 'degree': major.degree,
                       'name': major.name, 'mode': major.mode})

    return create_response(majors, 200, '*')
