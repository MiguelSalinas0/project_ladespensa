from flask import render_template, url_for, request, redirect, session, flash

from app import bp
from app.api.api_producto import *


@bp.route('/lista_productos')
def listado():
    if "id" in session:
        productos, error = get_all_prod()
        if error == None:
            session['bandera'] = False
            return render_template('lista_productos.html', productos=productos)
    else:
        return redirect(url_for("bp.login"))


@bp.route('/detalle', methods=['POST'])
def detalle():
    session['id'] = request.form['id']
    prod, error = get_prod_id(request.form['id'])
    productos, error = get_all_prod()
    if error == None:
        session['bandera'] = True
        return render_template('lista_productos.html', productos=productos, producto=prod)


@bp.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        if request.form['submit'] == 'cancelar':
            return redirect(url_for("bp.listado"))
        else:
            ide = session.get('id')
            prod, error = get_prod_id(ide)
            if error == None:
                prod_info = {}
                prod_info['id'] = session.get('id')
                prod_info['codigo'] = request.form['codigo']
                prod_info['nombre'] = request.form['nombre']
                prod_info['stock'] = request.form['stock']
                prod_info['detalle'] = request.form['detalle']
                prod_info['categoria'] = request.form['categoria']
                prod_info['codigo'] = request.form['codigo']
                prod_info['precio'] = request.form['precio']
                error = update_prod(prod_info)
                if error == None:
                    flash("Se editó exitosamente", category="success")
                    return redirect(url_for("bp.listado"))
                else:
                    flash("Ocurrió un error al editar el producto", category="error")
                    return redirect(url_for("bp.listado"))


@bp.route('/nuevo')
def nuevo():
    if session.get("usr") == 'admin':
        return render_template('nuevo.html')
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for("bp.index"))


@bp.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        prod_info = {}
        prod_info['codigo'] = request.form['codigo']
        prod_info['nombre'] = request.form['nombre']
        prod_info['stock'] = request.form['stock']
        prod_info['detalle'] = request.form['detalle']
        prod_info['categoria'] = request.form['categoria']
        prod_info['codigo'] = request.form['codigo']
        prod_info['precio'] = request.form['precio']
        error = insert_prod(prod_info)
        if error == None:
            flash("Se guardó exitosamente", category="success")
            return redirect(url_for("bp.nuevo"))
        else:
            flash("Ocurrió un error al agregar el nuevo registro", category="error")
            return redirect(url_for("bp.nuevo"))