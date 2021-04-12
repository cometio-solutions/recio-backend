"""Entrypoint for recio app"""
from rest.app import create_app, setup_database


app = create_app()
setup_database(app)

app.run(host='0.0.0.0')
