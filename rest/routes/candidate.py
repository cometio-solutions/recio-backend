"""
Endpoints connected with candidates
"""
import logging

from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.candidate import Candidate

candidate_url = Blueprint('candidate', __name__)


@candidate_url.route('/<candidate_pesel>', methods=['GET'])
def get_candidate(candidate_pesel):
    """
    Endpoint returns all available information about specific candidate
    :returns: flask response containing json with candidate data
    """
    logging.info("Getting candidate data")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is not specified!")
        return response

    if role != 'editor' or role != 'admin':
        logging.warning("Role is not an editor!")
        return create_response(
            {"error": "Tylko edytor moze otrzymac informacje o kandydacie."},
            403,
            '*'
        )

    data = dict()
    candidate = Candidate.filter_by(pesel=candidate_pesel)
    if len(candidate) == 0:
        logging.warning("No such user with given pesel!")
        return create_response({"error": "Nie ma urzytkownika o podanym peselu!"}, 404, '*')

    data['data'] = Candidate.to_json(candidate[0])

    return create_response(data, 200, '*')
