from datetime import datetime
from flask import Flask, flash, request, render_template, session, redirect, url_for
from api.api_producto import *
from api.api_venta import *

app = Flask(__name__)
app.secret_key = "ffgghhllmm"


@app.route('/inicio')
def inicio():
    session['items'] = []
    session['bandera'] = False
    return render_template('index.html')


@app.route('/')
def index():
    session['bandera'] = False
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/lista_productos')
def listado():
    productos, error = get_all_prod()
    if error == None:
        session['bandera'] = False
        return render_template('lista_productos.html', productos=productos)


@app.route('/detalle', methods=['POST'])
def detalle():
    session['id'] = request.form['id']
    prod, error = get_prod_id(request.form['id'])
    productos, error = get_all_prod()
    if error == None:
        session['bandera'] = True
        return render_template('lista_productos.html', productos=productos, producto=prod)


@app.route('/editar', methods=['POST'])
def editar():
    if request.method == 'POST':
        if request.form['submit'] == 'cancelar':
            return redirect(url_for("listado"))
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
                    return redirect(url_for("listado"))
                else:
                    flash("Ocurrió un error al editar el producto",
                          category="error")
                    return redirect(url_for("listado"))


@app.route('/nuevo')
def nuevo():
    return render_template('nuevo.html')


@app.route('/guardar', methods=['POST'])
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
            return redirect(url_for("nuevo"))
        else:
            flash("Ocurrió un error al agregar el nuevo registro", category="error")
            return redirect(url_for("nuevo"))


@app.route('/venta')
def venta():
    return render_template('venta.html', items=session.get('items'))


@app.route('/agregar_item', methods=['POST'])
def agregar_item():
    if request.method == 'POST':
        items = session.get('items')
        item = {}
        cant = int(request.form['cantidad'])
        prod, error = get_prod_cod(request.form['codigo'])
        if error == None:
            if cant > int(prod.get('stock')) or prod.get('stock') == 0:
                flash(f"Imposible agregar, no hay stock suficiente. Stock actual: {prod.get('stock')}", category="error")
                return redirect(url_for("venta"))
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
                totalVenta = 0
                for it in session.get('items'):
                    totalVenta = totalVenta + it['total']
                return render_template('venta.html', items=session.get('items'), totalVenta=totalVenta)
        else:
            flash("No se encontró el producto", category="error")
            return redirect(url_for("venta"))


@app.route('/eliminar_item', methods=['POST'])
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
        totalVenta = 0
        for it in session.get('items'):
            totalVenta = totalVenta + it['total']
        return render_template('venta.html', items=session.get('items'), totalVenta=totalVenta)


@app.route('/generarVenta', methods=['POST'])
def generarVenta():
    totalVenta = 0.0
    venta = {}
    for item in session.get('items'):
        error = update_stock(item['codigo'], item['cantidad'])
        totalVenta = totalVenta + item['total']
    venta['fecha'] = datetime.now()
    venta['total'] = totalVenta
    error = insert_vent(venta)
    if error == None:
        flash('La venta se realizó exitosamente', category='success')
    return redirect(url_for("inicio"))


@app.route('/historial_ventas')
def historial_ventas():
    ventas, error = get_all_ven()
    if error == None:
        return render_template('historial_ventas.html', ventas=ventas)
    

@app.route('/informes')
def informes():
    return render_template('informes.html')


def pagina_no_encontrada(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True)
