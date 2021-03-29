"""Entrypoint for recio app"""
import json
from rest.app import create_app, setup_database


app = create_app()
setup_database(app)


@app.route('/')
def hello():
    """
    An Example endpoint.
    :returns: response with {app: recio} and status 200
    """
    data = {"app": "recio"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


app.run(host='0.0.0.0')
