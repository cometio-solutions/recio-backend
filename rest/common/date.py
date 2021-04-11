"""This module contains common operation connected with datetime"""
from datetime import datetime


def datetime_from_string(date_string):
    """
    Returns datetime from string formatted like: 2021-01-01
    :param date_string: formatted string
    :return: datetime corresponding to date_string
    """
    return datetime.strptime(date_string, '%Y-%m-%d')
