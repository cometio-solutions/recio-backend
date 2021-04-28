"""This module contains endpoints connected with point limit"""
import sys
import logging
from datetime import date
from flask import Blueprint, request
from sqlalchemy.exc import SQLAlchemyError
from rest.common.token import handle_request_token
from rest.common.response import create_response
from rest.models.candidate_recruitment import CandidateRecruitment, RecruitmentStatus
from rest.models.recruitment import Recruitment
from rest.db import db

point_limit_url = Blueprint('point-limit', __name__)


@point_limit_url.route('', methods=['POST', 'OPTIONS'])
def calculate_point_limit():
    """
    Calculates point limit for every recruitment that has ended
    :return: flask Response with operation result
    """
    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', 'content-type, token')

    role, response = handle_request_token(request)

    if role is None:
        return response

    try:
        recruitments = Recruitment.query.filter_by(point_limit=None)\
                                        .filter(Recruitment.end_date <= date.today())
        for recruitment in recruitments:
            candidates = CandidateRecruitment.query.filter_by(recruitment_id=recruitment.id)\
                                                    .order_by(CandidateRecruitment.points.desc())
            places_left = recruitment.slot_limit
            point_limit = 0
            for candidate in candidates:
                if places_left > 0 and candidate.is_paid:
                    candidate.status = RecruitmentStatus.QUALIFIED
                    places_left -= 1
                    if places_left == 0:
                        point_limit = candidate.points
                else:
                    candidate.status = RecruitmentStatus.NOT_QUALIFIED
            recruitment.point_limit = point_limit

        db.session.commit()
    except (AttributeError, SQLAlchemyError) as exception:
        logging.error(exception, file=sys.stderr)
        return create_response({"error": "Nie udało się obliczyć progów."}, 400, "*")

    return create_response({"message": "Wyliczono progi rekrutacyjne"}, 200, "*")


@point_limit_url.route('/<recruitment_id>', methods=['GET', 'OPTIONS'])
def get_point_limits(recruitment_id):
    """
    Returns point limit for recruitment with given id, and for all connected recruitment
    :return: flask Response with list of recruitments point limits
    """
    if request.method == 'OPTIONS':
        return create_response({}, 200, '*', 'content-type, token')

    role, response = handle_request_token(request)

    if role is None:
        return response

    point_limits = {}
    try:
        recruitment = Recruitment.query.get(recruitment_id)
        # handle previous recruitment
        current_recruitment = recruitment
        print(current_recruitment, file=sys.stderr)
        while current_recruitment is not None:
            point_limits[current_recruitment.cycle_number] = current_recruitment.point_limit
            current_recruitment = current_recruitment.previous_recruitment
            print(current_recruitment, file=sys.stderr)
        # handel next recruitment
        current_recruitment = recruitment.next_recruitment
        print(current_recruitment, file=sys.stderr)
        while current_recruitment is not None:
            point_limits[current_recruitment.cycle_number] = current_recruitment.point_limit
            current_recruitment = current_recruitment.next_recruitment
            print(current_recruitment, file=sys.stderr)
    except (AttributeError, SQLAlchemyError) as exception:
        print(exception, file=sys.stderr)
        return create_response({"error": "Nie udało się pobrać progów rekrutacyjnych."}, 400, "*")

    data = [{"point_limit": value, "cycle_number": key} for key, value in point_limits.items()]

    return create_response(data, 200, "*")
