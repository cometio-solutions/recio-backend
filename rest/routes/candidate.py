"""
Endpoints connected with candidates
"""
import logging

from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.candidate import Candidate
from rest.models.candidate_recruitment import CandidateRecruitment
from rest.models.recruitment import Recruitment

candidate_url = Blueprint('candidate', __name__)


@candidate_url.route('/<candidate_pesel>', methods=['GET', 'OPTIONS'])
def get_candidate(candidate_pesel):
    """
    Endpoint returns all available information about specific candidate
    :returns: flask response containing json with candidate data
    """
    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', 'content-type, token')

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


@candidate_url.route('/migration/<candidate_pesel>', methods=['GET', 'OPTIONS'])
def get_candidate_migration(candidate_pesel):
    """
    Endpoint returns candidate's recruitment history
    :return: flask response containing json with recruitment history
    """
    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', 'content-type, token')

    logging.info("Getting recruitment data")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is not specified!")
        return response

    data = dict()
    candidate_recruitments = CandidateRecruitment.query\
        .filter_by(candidate_pesel=candidate_pesel).all()
    if len(candidate_recruitments) == 0:
        logging.warning("No such user with given pesel!")
        return create_response({"error": "Nie ma urzytkownika o podanym peselu!"}, 404, '*')

    recruitments = [Recruitment.query.filter_by(id=can_rec.recruitment_id).first()
                    for can_rec in candidate_recruitments]

    data['data'] = [Recruitment.to_json(rec, len(rec.candidate_recruitments))
                    for rec in recruitments]

    assert len(data['data']) == len(candidate_recruitments)

    for idx in range(len(data['data'])):
        data['data'][idx]['status'] = candidate_recruitments[idx].status.value

    return create_response(data, 200, '*')
