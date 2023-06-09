from db.db import get_db


def get_all_ven():
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM venta')
    ventas = cur.fetchall()
    vents = []
    for row in ventas:
        prod = dict(zip(('id', 'fecha', 'total'), row))
        vents.append(prod)
    return vents, error


def insert_vent(vent_info: dict):
    error = None
    con, cur = get_db()
    try:
        cur.execute('INSERT INTO venta (fecha, total) ' +
                    ' VALUES (?,?)', (vent_info.get('fecha'),
                                      vent_info.get('total')))
        con.commit()
    except Exception as E:
        con.rollback()
        print(f"Unexpected {E=}, {type(E)=}")
        error = {'error': 'Error grabando venta: ' + str(E)}
    return error


def get_rango(fecha_inicial, fecha_final):
    error = None
    con, cur = get_db()
    cur.execute('SELECT * FROM venta WHERE fecha BETWEEN ? and ?',
                (fecha_inicial, fecha_final,))
    ventas = cur.fetchall()
    vents = []
    for row in ventas:
        prod = dict(zip(('id', 'fecha', 'total'), row))
        vents.append(prod)
    return vents, error


def get_mes(mes):
    error = None
    con, cur = get_db()
    cur.execute("SELECT * FROM venta WHERE strftime('%Y-%m', fecha) = ?", (mes,))
    ventas = cur.fetchall()
    vents = []
    for row in ventas:
        prod = dict(zip(('id', 'fecha', 'total'), row))
        vents.append(prod)
    return vents, error
