import os
import json
from flask import Flask
import pymysql

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

conf = {
    "host": os.environ['HOST'],
    "port": int(os.environ['PORT']),
    "user": os.environ['USER'],
    "passwd": os.environ['PASSWORD'],
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "database": os.environ['DATABASE']
}

conn = pymysql.connect(**conf)
cursor = conn.cursor()
cursor.execute("SHOW TABLES")

print(cursor.fetchall())


@app.route('/')
def hello():
    data = {"app": "recio"}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
