import sqlite3
from flask import Flask, g

app = Flask(__name__)

DATABASE = 'C:/Users/w10-21h2/Desktop/project_ladespensa/instance/ladespensa.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return db, cursor


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
