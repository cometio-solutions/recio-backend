""" This module contains health check endpoints for REST API """
from datetime import datetime
import requests
from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError

from rest.common.response import create_response
from rest.db import db

healthcheck_url = Blueprint('healthcheck', __name__)


@healthcheck_url.route('', methods=['GET'])
def get_healthcheck():
    """
    Check status of REST API services
    :return: flask Response containing json with REST API status
    """

    swagger_ui_url = "http://134.122.71.130:8001/"

    data = {
        "time_stamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "database": "up",
        "swagger": "up"
    }

    try:
        db.get_engine().execute("SELECT 1")
    except SQLAlchemyError:
        data["database"] = "down"

    try:
        requests.get(swagger_ui_url)
    except requests.exceptions.RequestException:
        data["swagger"] = "down"

    return create_response(data, 200, '*')
