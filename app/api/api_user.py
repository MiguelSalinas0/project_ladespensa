import hashlib
from ..db.db import get_db


def usr_login(user: str, clave: str):
    error = None
    con, cur = get_db()
    try:
        cur.execute(
            "select id, nombre_usr, password from user where NOMBRE_USR = ?", (user,)
        )
        usuario = cur.fetchone()
        if usuario is None:
            error = {"error": "usuario o contraseña inválida"}
            return {}, error
        usuario = dict(zip(("id", "nombre_usr", "password"), usuario))
        result = hashlib.md5(bytes(clave, encoding="utf-8"))
        if result.hexdigest() == usuario.get("password"):
            return {
                "ID": usuario.get("id"),
                "NOMBRE": usuario.get("nombre_usr"),
            }, error
        else:
            error = {"error": "usuario o contraseña inválida"}
            return {}, error
    except Exception as e:
        error = {"error": "Error en el servidor"}
        return {}, error
    # finally:
    #     con.commit()
    #     con.close()
