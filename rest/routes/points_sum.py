"""This module contains endpoint for getting recruitment points of candidates"""
import logging
from flask import Blueprint, request
from rest.common.token import handle_request_token
from rest.common.response import create_response
from rest.models.candidate_recruitment import CandidateRecruitment


points_sum_url = Blueprint('points', __name__)


@points_sum_url.route('', methods=['GET', 'OPTIONS'])
def get_points_sum():
    if request.method == 'OPTIONS':
        logging.info("Handle options")
        return create_response({}, 200, '*', 'content-type, token')

    logging.info("Getting recruitment points sum")

    role, response = handle_request_token(request)

    if role is None:
        logging.warning("Role is None!")
        return response

    points = {}
    for rec in CandidateRecruitment.query.all():
        if rec.points not in points:
            points[rec.points] = 1
        else:
            points[rec.points] += 1

    points_sum = []
    for k, v in points.items():
        points_sum.append({'points': k, 'numberOfStudents': v})

    create_response(points_sum, 200, '*')
