"""This module contains endpoint for getting origins of candidates"""
import logging
from flask import Blueprint, request
from rest.common.response import create_response
from rest.common.token import handle_request_token
from rest.models.candidate import Candidate

origins_url = Blueprint('origins', __name__)


@origins_url.route('', methods=['GET', 'OPTIONS'])
def get_origins():
    """
    Collects summarises of all candidates origins.
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
    if request.method == 'OPTIONS':
        logging.info('Handling options')
        return create_response({}, 200, '*', 'content-type, token')

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

    for candidate in Candidate.query.all():
        country = candidate.country.capitalize()

        if country == 'Polska':
            region = candidate.region.capitalize().replace(' ', '')

            try:
                origins[region] += 1
            except KeyError:
                logging.warning('Unknown candidate region: %s', region)
        else:
            origins['Inne'] += 1

        return create_response(origins, 200, '*')
