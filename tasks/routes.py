from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProcessTaskForm

import sqlite3
from datetime import date

BASE_DATOS = './data/tasks.db'

def dict_factory(cursor, row):
    d = {}
    for ix, col in enumerate(cursor.description):
        d[col[0]] = row[ix]
    return d

def dbQuery(consulta, *args):
    conn = sqlite3.connect(BASE_DATOS)
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    rows = cursor.execute(consulta, args).fetchall()
    
    if len(rows) == 1:
        rows = rows[0]
    elif len(rows) == 0:
        rows = None
    
    conn.commit()
    conn.close()
    return rows

@app.route("/")
def index():
    datos = dbQuery('SELECT titulo, descripcion, fecha, id FROM tareas;')

    if datos:
        if isinstance(datos, dict):
            datos = [datos]
    else:
        datos = []

    return render_template("index.html", registros=datos)


@app.route("/newtask", methods=['GET', 'POST'])
def newtask():
    form = TaskForm(request.form)

    if request.method == 'GET':
        return render_template("task.html", form=form)
    
    if form.validate():
        title = request.values.get('title')
        desc = request.values.get('description')
        fx = request.values.get('fx')

        consulta = '''
        INSERT INTO tareas (titulo, descripcion, fecha)
                    VALUES(?, ?, ?);
        '''
        dbQuery(consulta, title, desc, fx)

        return redirect(url_for("index"))
    else:
        return render_template("task.html", form=form)

@app.route("/processtask", methods=['GET', 'POST'])
def processtask():
    form = ProcessTaskForm(request.form)
    if request.method == 'GET':
        ix = request.values.get('ix')
        if ix:
            registroAct = dbQuery('SELECT titulo, descripcion, fecha, id FROM tareas WHERE id = ?;', ix)
           
            if registroAct:
                if registroAct['fecha']:
                    fechaTarea = date(int(registroAct['fecha'][:4]), int(registroAct['fecha'][5:7]), int(registroAct['fecha'][8:]))
                else:
                    fechaTarea = None
                accion = ''  
                if 'btnModificar' in request.values:
                    accion = 'M'
                if 'btnBorrar' in request.values:
                    accion = 'B'
                        
                form = ProcessTaskForm(data={'ix': ix, 'title': registroAct['titulo'], 'description': registroAct['descripcion'], 'fx': fechaTarea, 'btn': accion})
                
            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for('index'))

    if form.btn.data == 'B':
        ix = int(request.values.get('ix'))
        consulta = '''
            DELETE FROM tareas
            WHERE id = ?;
        ''' 
        dbQuery(consulta, ix)

        return redirect(url_for('index'))
    
    if form.btn.data == 'M':
        if form.validate():
            ix = int(request.values.get('ix'))
            consulta = '''
                UPDATE tareas
                SET titulo = ?, descripcion = ?, fecha = ?
                WHERE id = ?;
            '''
            dbQuery(consulta,
                    request.values.get('title'),
                    request.values.get('description'),
                    request.values.get('fx'),
                    ix)

            return redirect(url_for("index"))

        return render_template("processtask.html", form=form)

    print('method:', request.method)
    print('parametros:', request.values)