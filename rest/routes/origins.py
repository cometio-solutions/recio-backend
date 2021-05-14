"""This module contains endpoint for getting origins of candidates"""
import logging
import sys

from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, request
from rest.common.response import create_response, options_response
from rest.common.token import handle_request_token
from rest.models.candidate import Candidate
from rest.models.recruitment import Recruitment
from rest.models.candidate_recruitment import CandidateRecruitment

origins_url = Blueprint('origins', __name__)


@origins_url.before_request
def handle_options():
    """
    Handles OPTIONS method before recruitment endpoint
    :return: flask Response object with status 200 if the method is OPTIONS, else None
    """
    return options_response(request)


@origins_url.route('/<recruitment_id>', methods=['GET', 'OPTIONS'])
def get_origins(recruitment_id):
    """
    Collects origin of all candidates with a certain recruitment id.

    In JSON format, where value in each is an Integer:
    {
        'Dolnośląskie'
        'Kujawsko-pomorskie'
        'Lubelskie'
        'Lubuskie'
        'Łódzkie'
        'Małopolskie'
        'Mazowieckie'
        'Opolskie'
        'Podkarpackie'
        'Podlaskie'
        'Pomorskie'
        'Śląskie'
        'Świętokrzyskie'
        'Warmińsko-mazurskie'
        'Wielkopolskie'
        'Zachodniopomorskie'
        'Inne'
    }

    The names of regions and countries must start with capital letter,
    and in case of being split (by '-') there shouldn't be spaces between.
    Although currently for 'Warmińsko-mazurskie' and 'Kujawsko-pomorskie'
    it is checked if the first part is correct (before '-').

    :return: flask Response containing JSON with all origins
    """
    logging.info('Getting all origins')

    role, response = handle_request_token(request)

    if role is None:
        logging.warning('Role is None!')
        return response

    origins = {
        'Dolnośląskie': 0,
        'Kujawsko-pomorskie': 0,
        'Lubelskie': 0,
        'Lubuskie': 0,
        'Łódzkie': 0,
        'Małopolskie': 0,
        'Mazowieckie': 0,
        'Opolskie': 0,
        'Podkarpackie': 0,
        'Podlaskie': 0,
        'Pomorskie': 0,
        'Śląskie': 0,
        'Świętokrzyskie': 0,
        'Warmińsko-mazurskie': 0,
        'Wielkopolskie': 0,
        'Zachodniopomorskie': 0,
        'Inne': 0
    }

    try:
        if not Recruitment.query.filter_by(id=recruitment_id).first():
            logging.warning('Nie znaleziono rekrutacji o takim ID')
            return create_response({'error': 'Nie znaleziono podanej rekrutacji'}, 404, '*')

        for candidate_recruitment in \
                CandidateRecruitment.query.filter_by(recruitment_id=recruitment_id):

            candidate = Candidate.query.get(candidate_recruitment.candidate_pesel)

            country = candidate.country.capitalize()

            if country == 'Polska':
                region = candidate.region.capitalize().replace(' ', '')

                try:
                    origins[region] += 1
                except KeyError:
                    logging.warning('Unknown candidate region: %s', region)

            else:
                origins['Inne'] += 1

    except SQLAlchemyError as exception:
        logging.error(exception, file=sys.stderr)
        return create_response({'error': 'Błąd podczas pobierania pochodzenia'}, 400, '*')

    return create_response(origins, 200, '*')
