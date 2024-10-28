from ..db.db import get_db


def get_all_ven():
    con, cur = None, None
    try:
        con, cur = get_db()
        cur.execute("SELECT * FROM venta_cabecera")
        ventas = cur.fetchall()
        vents = [dict(zip(("id", "fecha", "total"), row)) for row in ventas]
        return vents, None
    except Exception as e:
        error = str(e)
        return None, error
    # finally:
    #     if cur:
    #         cur.close()
    #     if con:
    #         con.close()


def insert_vent(vent_info: dict):
    con, cur = None, None
    last_id = None
    error = None
    try:
        con, cur = get_db()
        cur.execute(
            "INSERT INTO venta_cabecera (fecha, total) VALUES (?, ?)",
            (vent_info.get("fecha"), vent_info.get("total")),
        )
        con.commit()
        last_id = cur.lastrowid
    except Exception as e:
        if con:
            con.rollback()
        error = f"Error grabando venta: {str(e)}"
    # finally:
    #     if cur:
    #         cur.close()
    #     if con:
    #         con.close()
    return {"last_id": last_id}, error


def insert_detalle(venta_id: int, articulo_id: int, cantidad_art: int):
    con, cur = None, None
    error = None
    try:
        con, cur = get_db()
        cur.execute(
            "INSERT INTO venta_detalle (venta_id, articulo_id, cantidad_art) VALUES (?, ?, ?)",
            (venta_id, articulo_id, cantidad_art),
        )
        con.commit()
    except Exception as e:
        if con:
            con.rollback()
        error = f"Error grabando detalle de venta: {str(e)}"
    # finally:
    #     if cur:
    #         cur.close()
    #     if con:
    #         con.close()
    return error

















def get_detalle(venta_id: int):
    con, cur = None, None
    error = None
    detalle = []
    try:
        con, cur = get_db()
        cur.execute(
            "SELECT * FROM venta_detalle vd JOIN producto pr ON vd.articulo_id = pr.codigo WHERE vd.venta_id = ?",
            (venta_id),
        )
        detalle = cur.fetchall()
        con.commit()
    except Exception as e:
        error = str(e)
        return [], error
    details = []
    for row in detalle:
        det = dict(zip(("cantidad_art", "nombre", "detalle"), row))
        details.append(det)
    return details, error


# def get_rango(fecha_inicial, fecha_final):
#     error = None
#     con, cur = get_db()
#     cur.execute(
#         "SELECT * FROM venta_cabecera WHERE fecha BETWEEN ? and ?",
#         (
#             fecha_inicial,
#             fecha_final,
#         ),
#     )
#     ventas = cur.fetchall()
#     vents = []
#     for row in ventas:
#         prod = dict(zip(("id", "fecha", "total"), row))
#         vents.append(prod)
#     return vents, error


def get_rango(fecha_inicial, fecha_final):
    error = None
    ventas = []
    try:
        con, cur = get_db()
        cur.execute(
            "SELECT * FROM venta_cabecera WHERE fecha BETWEEN ? AND ?",
            (fecha_inicial, fecha_final)
        )
        ventas = cur.fetchall()
    except Exception as e:
        error = str(e)
    # finally:
    #     con.close()
    vents = []
    for row in ventas:
        prod = dict(zip(("id", "fecha", "total"), row))
        vents.append(prod)
    return vents, error


# def get_mes(mes):
#     error = None
#     con, cur = get_db()
#     cur.execute(
#         "SELECT * FROM venta_cabecera WHERE strftime('%Y-%m', fecha) = ?", (mes,)
#     )
#     ventas = cur.fetchall()
#     vents = []
#     for row in ventas:
#         prod = dict(zip(("id", "fecha", "total"), row))
#         vents.append(prod)
#     return vents, error


def get_mes(mes):
    error = None
    ventas = []
    try:
        con, cur = get_db()
        cur.execute(
            "SELECT * FROM venta_cabecera WHERE strftime('%Y-%m', fecha) = ?", (mes,)
        )
        ventas = cur.fetchall()
    except Exception as e:
        error = str(e)
    # finally:
    #     con.close()
    vents = []
    for row in ventas:
        prod = dict(zip(("id", "fecha", "total"), row))
        vents.append(prod)
    return vents, error
