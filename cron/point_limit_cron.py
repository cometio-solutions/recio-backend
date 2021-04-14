"""This module contains code that should be executed every day to calculate point limits"""
import json
from datetime import datetime
import requests


data = {'email': 'editor@agh.edu.pl', 'password': 'editor'}
response = requests.post('http://web:5000/user/auth', json=data)
editor_login = json.loads(response.content.decode('utf-8'))
requests.post('http://web:5000/recruitment/point-limit',
              headers={'token': editor_login['token']})
print(f'{datetime.now()}: Cron job done')
