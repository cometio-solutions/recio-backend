"""This module contains endpoints connected with recruitment"""
from datetime import datetime

from flask import Blueprint, request

from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.recruitment import Recruitment

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

    recruitment_requests = Recruitment.query.all()
    data = dict()
    data['data'] = [{
        'id': rec.id,
        'major_id': rec.major_id,
        'end_date': rec.end_date.strftime("%m/%d/%Y, %H:%M:%S"),
        'cycle_number': rec.cycle_number,
        'slot_limit': rec.slot_limit,
        'point_limit': rec.point_limit,
        'is_active': bool(rec.end_date > datetime.now()),
        'faculty': rec.major.faculty,
        'degree': rec.major.degree,
        'major_name': rec.major.name,
        'major_mode': rec.major.mode
    } for rec in recruitment_requests]
    return create_response(data, 200, '*')
