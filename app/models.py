from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    detalle = db.Column(db.String(120), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    precio = db.Column(db.Float, nullable=False)


class Venta(db.Model):
    __tablename__ = 'venta'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
