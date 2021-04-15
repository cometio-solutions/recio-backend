"""This module contains endpoints connected with point limit"""
import sys
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
        print(exception, file=sys.stderr)
        return create_response({"error": "Nie udało się obliczyć progów."}, 400, "*")

    return create_response({"message": "Wyliczono progi rekrutacyjne"}, 200, "*")
