from flask import Flask
import pymysql

app = Flask(__name__)

conf = {
    "host": "db",
    "port": 3306,
    "user": "user",
    "passwd": "password",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "database": "recio"
}

conn = pymysql.connect(**conf)
cursor = conn.cursor()
cursor.execute("SHOW TABLES")

print(cursor.fetchall())

@app.route('/')
def hello():
    return "Hello World!"
