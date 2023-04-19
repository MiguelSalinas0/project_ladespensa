from db.db import get_db


def get_prod_cod(prod_cod):
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM producto WHERE codigo=?', (prod_cod,))
    prod = cur.fetchone()
    if prod == None:
        prod = {}
        return prod, error
    else:
        prod = dict(zip(('id', 'codigo', 'nombre', 'stock',
                    'detalle', 'categoria', 'precio'), prod))
    con.commit()
    return prod, error


def get_prod_id(prod_id):
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM producto WHERE id=?', (prod_id,))
    prod = cur.fetchone()
    if prod == None:
        prod = {}
        return prod, error
    else:
        prod = dict(zip(('id', 'codigo', 'nombre', 'stock',
                    'detalle', 'categoria', 'precio'), prod))
    con.commit()
    return prod, error


def get_all_prod():
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM producto')
    productos = cur.fetchall()
    prods = []
    for row in productos:
        prod = dict(zip(('id', 'codigo', 'nombre', 'stock',
                    'detalle', 'categoria', 'precio'), row))
        prods.append(prod)
    return prods, error


def insert_prod(prod_info: dict):
    error = None
    con, cur = get_db()
    try:
        cur.execute('INSERT INTO producto (codigo, nombre, stock, detalle, categoria, precio) ' +
                    ' VALUES (?,?,?,?,?,?)', (prod_info.get('codigo'),
                                              prod_info.get('nombre'),
                                              prod_info.get('stock'),
                                              prod_info.get('detalle'),
                                              prod_info.get('categoria'),
                                              prod_info.get('precio')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando producto: ' + str(E)}
    return error


def update_prod(prod_info: dict):
    error = None
    con, cur = get_db()
    try:
        cur.execute('UPDATE producto SET codigo = ?, nombre = ?, stock = ?, detalle = ?, categoria = ?, precio = ?' +
                    'WHERE id = ?', (prod_info.get('codigo'),
                                     prod_info.get('nombre'),
                                     prod_info.get('stock'),
                                     prod_info.get('detalle'),
                                     prod_info.get('categoria'),
                                     prod_info.get('precio'),
                                     prod_info.get('id')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error actualizando el producto: ' + str(E)}
    return error


def update_stock(cod, cant: int):
    error = None
    con, cur = get_db()
    prod, error = get_prod_cod(cod)
    nuevoStock = int(prod.get('stock')) - cant
    try:
        cur.execute('UPDATE producto SET stock = ? WHERE codigo = ?',
                    (nuevoStock, prod.get('codigo'),))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
    return error
