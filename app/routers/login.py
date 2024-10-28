from flask import render_template, url_for, request, redirect, session, flash

from app import bp
from app.api.api_user import *


@bp.route("/inicio")
def inicio():
    session["items"] = []
    session["bandera"] = False
    return render_template("index.html")


@bp.route("/")
def index():
    if "id" in session:
        return redirect(url_for("bp.inicio"))
    else:
        return render_template("login.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        if usuario and clave:
            datosUsr, error = usr_login(usuario, clave)
            if not error:
                if "ID" in datosUsr:
                    session["id"] = datosUsr["ID"]
                    session["usr"] = datosUsr["NOMBRE"]
                    nomUsuario = datosUsr["NOMBRE"]
                    flash(f"Inicio de sesión exitosa - { nomUsuario }", "info")
                    return redirect(url_for("bp.inicio"))
                else:
                    flash(f"Nombre de usuario y/o clave erroneos", "error")
                    return redirect(url_for("bp.login"))
            else:
                flash(error["error"], "error")
                return redirect(url_for("bp.login"))
        else:
            flash("Por favor ingrese tanto el nombre de usuario como la clave", "error")
            return render_template("login.html")
    else:
        return render_template("login.html")


@bp.route("/salir")
def salir():
    session["id"] = None
    session["usr"] = None
    return render_template("login.html")
