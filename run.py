from app import bp
from flask import Flask, render_template

from app.db.db import close_connection


def pagina_no_encontrada(error):
    return render_template('404.html'), 404


app = Flask(__name__)
app.secret_key = "ffgghhllmm"
app.register_blueprint(bp)
app.static_folder = 'app/static'
app.register_error_handler(404, pagina_no_encontrada)
app.teardown_appcontext(close_connection)

if __name__ == '__main__':
    app.run(debug=True)
