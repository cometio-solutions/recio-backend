"""Entrypoint for recio app"""
from rest.app import create_app, setup_database
from rest.common.settings import setup_logger

setup_logger()
app = create_app()
setup_database(app)

app.run(host='0.0.0.0')
