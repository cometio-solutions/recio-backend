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
    candidate = Candidate.get(pesel=candidate_pesel)
    if len(candidate) == 0:
        logging.warning("No such user with given pesel!")
        return create_response({"error": "Nie ma urzytkownika o podanym peselu!"}, 404, '*')

    data['data'] = Candidate.to_json(candidate[0])

    return create_response(data, 200, '*')


@candidate_url.route('/migration/<candidate_pesel>', methods=['GET'])
def get_candidate_migration(candidate_pesel):
    """
    Endpoint returns candidate's recruitment history
    :return: flask response containing json with recruitment history
    """
    logging.info("Getting recruitment data")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is not specified!")
        return response

    data = dict()
    candidate = CandidateRecruitment.filter_by(candidate_pesel=candidate_pesel)
    if len(candidate) == 0:
        logging.warning("No such user with given pesel!")
        return create_response({"error": "Nie ma urzytkownika o podanym peselu!"}, 404, '*')

    data['data'] = [Recruitment.to_json(rec,
                                        len(CandidateRecruitment
                                            .query
                                            .filter_by(recruitment_id=rec.id)
                                            .all()))
                    for rec in candidate.recruitment]

    return create_response(data, 200, '*')
