import sqlite3
from flask import g

DATABASE = 'D:/Proyectos/La Despensa/project_ladespensa/app/instance/ladespensa.db'


# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     cursor = db.cursor()
#     return db, cursor


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db, g.db.cursor()



# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
