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

    data = dict()
    candidate = Candidate.query.get(candidate_pesel)
    if candidate is None:
        logging.warning("No such user with given pesel!")
        return create_response({"error": "Nie ma urzytkownika o podanym peselu!"}, 404, '*')

    data['data'] = Candidate.to_json(candidate)

    return create_response(data, 200, '*')
