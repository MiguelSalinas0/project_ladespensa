from datetime import datetime
from flask import render_template, url_for, request, redirect, session, flash

from app import bp
from app.api.api_venta import *
from app.api.api_producto import *


@bp.route('/venta')
def venta():
    session['items'] = []
    totalVenta = 0.0
    return render_template('venta.html', totalVenta=totalVenta)


@bp.route('/agregar_item', methods=['POST'])
def agregar_item():
    if request.method == 'POST':
        items = session.get('items')
        item = {}
        cant = int(request.form['cantidad'])
        prod, error = get_prod_cod(request.form['codigo'])
        if error == None:
            if cant > int(prod.get('stock')) or prod.get('stock') == 0:
                flash(
                    f"Imposible agregar, no hay stock suficiente. Stock actual: {prod.get('stock')}", category="error")
                return redirect(url_for("bp.venta"))
            else:
                item['id'] = prod.get('id')
                item['codigo'] = prod.get('codigo')
                item['nombre'] = prod.get('nombre')
                item['precio'] = prod.get('precio')
                item['detalle'] = prod.get('detalle')
                item['categoria'] = prod.get('categoria')
                item['cantidad'] = cant
                item['total'] = float(prod.get('precio')) * cant
                items.append(item)
                session['items'] = items
                totalVenta = 0.0
                for it in session.get('items'):
                    totalVenta = totalVenta + it['total']
                return render_template('venta.html', items=session.get('items'), totalVenta=totalVenta)
        else:
            flash("No se encontró el producto", category="error")
            return redirect(url_for("bp.venta"))


@bp.route('/eliminar_item', methods=['POST'])
def eliminar_item():
    if request.method == 'POST':
        item = int(request.form['item'])
        encontrado = False
        indice = 0
        productos = session.get('items')
        while encontrado == False and indice < len(productos):
            if productos[indice]['id'] == item:
                del productos[indice]
                session['items'] = productos
                encontrado = True
            else:
                indice = indice + 1
        totalVenta = 0.0
        for it in session.get('items'):
            totalVenta = totalVenta + it['total']
        return render_template('venta.html', items=session.get('items'), totalVenta=totalVenta)


# @bp.route('/generarVenta', methods=['POST'])
# def generarVenta():
#     totalVenta = 0.0
#     venta = {}
#     articulos = session.get('items')
#     for item in articulos:
#         # error = update_stock(item['codigo'], item['cantidad'])
#         totalVenta = totalVenta + item['total']
#     venta['fecha'] = datetime.now()
#     venta['total'] = totalVenta
#     result = insert_vent(venta)
#     if result['error'] is None:
#         for item in articulos:
#             update_error = update_stock(item['codigo'], item['cantidad'])
#             detalle_err = insert_detalle(result['last_id'], item['codigo'], item['cantidad'])
#             if detalle_err == None and update_error == None:
#                 flash('La venta se realizó exitosamente', category='success')
#             else:
#                 flash("Ocurrió algún error", category='error')
#     else:
#         flash(result['error']['error'], category='error')
#     return redirect(url_for("bp.inicio"))





@bp.route('/generarVenta', methods=['POST'])
def generarVenta():
    totalVenta = 0.0
    venta = {}
    articulos = session.get('items', [])
    
    if not articulos:
        flash('No hay artículos en el carrito.', category='error')
        return redirect(url_for("bp.inicio"))

    for item in articulos:
        totalVenta += item['total']

    venta['fecha'] = datetime.now()
    venta['total'] = totalVenta
    result, error = insert_vent(venta)

    if error is None:
        # Se asume que update_stock y insert_detalle pueden devolver errores
        errores = []
        for item in articulos:
            update_error = update_stock(item['codigo'], item['cantidad'])
            detalle_err = insert_detalle(result['last_id'], item['codigo'], item['cantidad'])
            if update_error:
                errores.append(update_error)
            if detalle_err:
                errores.append(detalle_err)
        if errores:
            flash("Se encontraron errores durante el procesamiento de la venta.", category='error')
        else:
            flash('La venta se realizó exitosamente', category='success')
            session.pop('items', None)  # Limpiar el carrito si la venta fue exitosa
    else:
        flash(error, category='error')

    return redirect(url_for("bp.inicio"))


