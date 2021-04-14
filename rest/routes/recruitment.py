"""This module contains endpoints connected with recruitment"""
import sys
from sqlalchemy.exc import SQLAlchemyError 
from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.recruitment import Recruitment
from rest.models.candidate_recruitment import CandidateRecruitment

recruitment_url = Blueprint('recruitment', __name__)


@recruitment_url.before_request
def handle_options():
    """
    Handles OPTIONS method before recruitment endpoint
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    headers = 'content-type, token'

    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', headers)

    return None


@recruitment_url.route('', methods=['GET', 'OPTIONS'])
def get_all_recruitment_data():
    """
    Collects all available recruitment data from database
    JSON format:
    ```json
    {  "data" :
        [
            {
                'id'
                'major_id'
                'end_date'
                'cycle_number'
                'slot_limit'
                'point_limit'
                'is_active'
                'faculty'
                'degree'
                'major_name'
                'major_mode'
            },
            ...
        ]
    }
    ```
    :return: flask Response containing json with all recruitment data
    """

    role, response = handle_request_token(request)

    if role is None:
        return response

    data = dict()
    data['data'] = [Recruitment.to_json(rec) for rec in Recruitment.query.all()]
    return create_response(data, 200, '*')


@recruitment_url.route('/<recruitment_id>', methods=['GET', 'OPTIONS'])
def get_recruitment_with_candidates(recruitment_id):
    """
    Get recruitment with given id and all candidates
    :param id: id of recruitment
    :return: flask Response containing json with recruitment data
    """
    role, response = handle_request_token(request)

    if role is None:
        return response

    try:
        recruitment = Recruitment.query.filter_by(id=recruitment_id).first()
        if not recruitment:
            return create_response({"error": "Nie znaleziono podanej rekrutacji"}, 404, '*')
        data = dict()
        data = Recruitment.to_json(recruitment)
        data['candidates'] = [CandidateRecruitment.to_json(rec) for rec in
                              recruitment.candidate_recruitments]
    except (AttributeError, SQLAlchemyError) as exception:
        print(exception, file=sys.stderr)
        return create_response({"error": "Błąd podczas pobierania kandydatów."}, 400, '*')

    return create_response(data, 200, '*')
