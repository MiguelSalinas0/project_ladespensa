from flask import render_template, url_for, request, redirect, session, flash

from app import bp
from app.api.api_venta import *
from app.api.api_producto import *


@bp.route('/informes')
def informes():
    if session.get("usr") == 'admin':
        return render_template('informes.html')
    else:
        flash('No tiene autorización', category='error')
        return redirect(url_for("bp.index"))


@bp.route('/select_informe', methods=['POST'])
def select_informe():
    if request.method == 'POST':
        return render_template('informes.html', op=request.form['infoSel'])


# @bp.route('/get_informes', methods=['POST'])
# def get_informes():
#     if request.method == 'POST':
#         op = request.form['option']
#         if op == '1':
#             f1 = request.form['myDate1'] + ' 00:00:00'
#             f2 = request.form['myDate2'] + ' 23:59:59'
#             ventas, error = get_rango(f1, f2)
#             if error == None:
#                 return render_template('informes.html', op=op, ventas=ventas, f1=request.form['myDate1'], f2=request.form['myDate2'])
#         if op == '2':
#             totalDia = 0.0
#             f1 = request.form['myDate1'] + ' 00:00:00'
#             f2 = request.form['myDate1'] + ' 23:59:59'
#             ventas, error = get_rango(f1, f2)
#             if error == None:
#                 for item in ventas:
#                     totalDia = totalDia + item['total']
#                 return render_template('informes.html', op=op, ventas=ventas, f1=request.form['myDate1'], totalDia=totalDia)
#         if op == '3':
#             totalMes = 0.0
#             mes = request.form['myDate1']
#             ventas, error = get_mes(mes)
#             if error == None:
#                 for item in ventas:
#                     totalMes = totalMes + item['total']
#                 return render_template('informes.html', op=op, ventas=ventas, f1=request.form['myDate1'], totalMes=totalMes)


@bp.route('/get_informes', methods=['POST'])
def get_informes():
    if request.method == 'POST':
        op = request.form.get('option')
        if op == '1':
            f1 = request.form.get('myDate1') + ' 00:00:00'
            f2 = request.form.get('myDate2') + ' 23:59:59'
            ventas, error = get_rango(f1, f2)
            if error is None:
                return render_template('informes.html', op=op, ventas=ventas, f1=request.form.get('myDate1'), f2=request.form.get('myDate2'))
            else:
                flash(error, category='error')
                return redirect(url_for("bp.informes"))
        elif op == '2':
            totalDia = 0.0
            f1 = request.form.get('myDate1') + ' 00:00:00'
            f2 = request.form.get('myDate1') + ' 23:59:59'
            ventas, error = get_rango(f1, f2)
            if error is None:
                totalDia = sum(item['total'] for item in ventas)
                return render_template('informes.html', op=op, ventas=ventas, f1=request.form.get('myDate1'), totalDia=totalDia)
            else:
                flash(error, category='error')
                return redirect(url_for("bp.informes"))
        elif op == '3':
            totalMes = 0.0
            mes = request.form.get('myDate1')
            ventas, error = get_mes(mes)
            if error is None:
                totalMes = sum(item['total'] for item in ventas)
                return render_template('informes.html', op=op, ventas=ventas, f1=request.form.get('myDate1'), totalMes=totalMes)
            else:
                flash(error, category='error')
                return redirect(url_for("bp.informes"))
        else:
            flash("Invalid option", category='error')
            return redirect(url_for("bp.informes"))
    flash("Invalid request method", category='error') 
    return redirect(url_for("bp.inicio"))
