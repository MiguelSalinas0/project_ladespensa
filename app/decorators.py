from functools import wraps
from flask import flash, redirect, session, url_for

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash('No está iniciada la sesión', category='error')
            return redirect(url_for("bp.login"))
        return view_func(*args, **kwargs)
    return wrapper
