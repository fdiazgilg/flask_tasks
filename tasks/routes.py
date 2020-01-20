from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProccesTaskForm, EmployeeForm, ProccesEmployeeForm

import sqlite3
from datetime import date

BASE_DATOS = './data/{}'.format(app.config['DB_FILE'])

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
    registros = dbQuery('SELECT tareas.titulo, tareas.descripcion, tareas.fecha, tareas.id, empleados.name, empleados.apellidos FROM tareas LEFT JOIN empleados ON tareas.id_empleado = empleados.id')
    
    if registros:
        if isinstance(registros, dict):
            registros = [registros]
    else:
        registros = []
    return render_template("index.html", registros=registros) 



@app.route("/newtask", methods=['GET', 'POST'])
def newTask():
    consulta = """
        SELECT id, name, apellidos FROM empleados;
    """
    empleados = dbQuery(consulta)
    if empleados:
        if isinstance(empleados, dict):
            empleados = [empleados]
            mychoices = [(-1, 'Seleccione Empleado')]+[(e['id'], '{} {}'.format(e['name'], e['apellidos'])) for e in empleados]
    else:
        mychoices = [(-1, 'Seleccione Empleado')]
    
    form = TaskForm(request.form)
    form.updateChoices(mychoices)
    if request.method == 'GET':
        return render_template("task.html", form=form)

    if form.validate():
        title = request.values.get('title')
        desc = request.values.get('description')
        fx = request.values.get('fx')
        id_employee = request.values.get('id_employee')
        if id_employee == '-1':
            id_employee = '-'

        consulta = """
        INSERT INTO tareas (titulo, descripcion, fecha, id_empleado)
                    VALUES (?, ?, ?, ?);
        """
        dbQuery(consulta, title, desc, fx, id_employee)

        return redirect(url_for("index"))
    else:
        return render_template("task.html", form=form)

@app.route("/processtask", methods=['GET', 'POST'])
def proccesTask():
    form = ProccesTaskForm(request.form)

    if request.method == 'GET':
        ix = request.values.get('ix')
        if ix:
            registroAct = dbQuery('Select titulo, descripcion, fecha, id from tareas where id = ?;', ix)

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


                form = ProccesTaskForm(data={'ix': ix, 
                                             'title': registroAct['titulo'], 
                                             'description': registroAct['descripcion'], 
                                             'fx': fechaTarea, 
                                             'btn': accion})

            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for("index"))

    if form.btn.data == 'B':
        ix = int(request.values.get('ix'))
        consulta = """
            DELETE FROM tareas
                WHERE id = ?;
        """
        dbQuery(consulta, ix)

        return redirect(url_for('index'))
    
    if form.btn.data == 'M':
        if form.validate():
            ix = int(request.values.get('ix'))
            consulta = """
                UPDATE tareas
                SET titulo = ?, descripcion = ?, fecha = ?
                WHERE id = ?;
            """
            dbQuery(consulta, 
                    request.values.get('title'), 
                    request.values.get('description'), 
                    request.values.get('fx'), 
                    ix)

            return redirect(url_for("index"))
        return render_template("processtask.html", form=form)

@app.route("/employees")
def employees():
    registros = dbQuery('SELECT name, apellidos, email, id FROM empleados;')

    if registros:
        if isinstance(registros, dict):
            registros = [registros]
    else:
        registros = []

    return render_template("employees.html", registros=registros)

@app.route("/newemployee", methods=['GET', 'POST'])
def newEmployee():
    form = EmployeeForm(request.form)

    if request.method == 'GET':
        return render_template("employee.html", form=form)

    if form.validate():
        name = request.values.get('name')
        lastname = request.values.get('lastname')
        email = request.values.get('email')

        consulta = """
        INSERT INTO empleados (name, apellidos, email)
                    VALUES (?, ?, ?);
        """
        dbQuery(consulta, name, lastname, email)

        return redirect(url_for("employees"))
    else:
        return render_template("employee.html", form=form)

@app.route("/processemployee", methods=["GET", "POST"])
def proccesEmployee():
    form = ProccesEmployeeForm(request.form)

    if request.method == 'GET':
        id = request.values.get('ix')
        if id:
            registroAct = dbQuery('SELECT name, apellidos, email, id from empleados where id = ?;', id)

            if registroAct:
                accion = ''

                if 'btnModificar' in request.values:
                    accion = 'M'

                if 'btnBorrar' in request.values:
                    accion = 'B'

                form = ProccesEmployeeForm(data={'id': id, 
                                                  'name': registroAct['name'], 
                                                  'lastname': registroAct['apellidos'], 
                                                  'email': registroAct['email'], 
                                                  'btn': accion})

            return render_template("processemployee.html", form=form)                                
        else:
            return redirect(url_for("employees"))
    
    if form.btn.data == 'B':
        id = int(request.values.get('id'))
        consulta = """
            DELETE FROM empleados
             WHERE id = ?;
        """
        dbQuery(consulta, id)

        return redirect(url_for("employees"))

    if form.btn.data == 'M':
        if form.validate():
            id = int(request.values.get('id'))
            consulta = """
                UPDATE empleados
                   SET name = ?, apellidos = ?, email = ?
                 WHERE id = ?;
            """

            dbQuery(consulta,
                    request.values.get('name'), 
                    request.values.get('lastname'),
                    request.values.get('email'),
                    id)

            return redirect(url_for("employees"))
        return render_template("processemployee.html", form=form)