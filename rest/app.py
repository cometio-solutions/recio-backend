import os
from flask import Flask
import pymysql

app = Flask(__name__)

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
    return "Hello World!"
