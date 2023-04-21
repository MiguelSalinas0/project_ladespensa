import hashlib
from db.db import get_db


def usr_login(user: str, clave: str):
    error = None
    con, cur = get_db()
    cur.execute('select * from user where NOMBRE_USR = ?', (user,))
    usuario = cur.fetchone()
    if usuario == None:
        error = {'error': 'usuario o contraseña inválida'}
        con.commit()
        return {}, error
    else:
        usuario = dict(zip(('id', 'nombre_usr', 'password'), usuario))
        result = hashlib.md5(bytes(clave, encoding='utf-8'))
        if result.hexdigest() == usuario.get('password'):
            con.commit()
            return {'ID': usuario.get('id'), 'NOMBRE': usuario.get('nombre_usr')}, error
        else:
            error = {'error': 'usuario o contraseña inválida'}
            con.commit()
            return {}, error
