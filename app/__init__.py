from flask import Blueprint

bp = Blueprint('bp', __name__, template_folder='templates', static_folder='static')

from .routers import producto, venta, informes, login