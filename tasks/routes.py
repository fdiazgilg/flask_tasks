from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProcessTaskForm

import csv, sqlite3
from datetime import date

DATOS = './data/tareas.dat'
COPIA = './data/copia.dat'
BASE_DATOS = './data.tasks.db'

@app.route("/")
def index():
    #leer el fichero csv
    fTasks = open(DATOS, 'r')
    csvreader = csv.reader(fTasks, delimiter=',')
    datos = []

    for linea in csvreader:
        datos.append(linea)

    fTasks.close()
   
    if datos != []:
        datos.sort(key=lambda x: x[2])

    return render_template("index.html", registros=datos)


@app.route("/newtask", methods=['GET', 'POST'])
def newtask():
    form = TaskForm(request.form)

    if request.method == 'GET':
        return render_template("task.html", form=form)
    
    if form.validate():
        fTasks = open(DATOS, 'a')
        csvwriter = csv.writer(fTasks, delimiter=",", quotechar='"', lineterminator='\r')

        title = request.values.get('title')
        desc = request.values.get('description')
        date = request.values.get('date')

        csvwriter.writerow([title, desc, date])

        fTasks.close()

        return redirect(url_for("index"))

    else:
        return render_template("task.html", form=form)


    print('method:', request.method)
    print('parametros:', request.values)


@app.route("/processtask", methods=['GET', 'POST'])
def processtask():
    form = ProcessTaskForm(request.form)
    if request.method == 'GET':
        fTasks = open(DATOS, 'r')
        csvreader = csv.reader(fTasks, delimiter=",", quotechar='"')

        registroAct = None
        ilinea = 1
        ix = int(request.values.get('ix'))
        for linea in csvreader:
            if ilinea == ix:
                registroAct = linea
                break
            ilinea += 1

        if registroAct:
            if registroAct[2]:
                fechaTarea = date(int(registroAct[2][:4]), int(registroAct[2][5:7]), int(registroAct[2][8:]))
            else:
                fechaTarea = None
            
            accion = ''
            
            if 'btnModificar' in request.values:
                accion = 'M'
            if 'btnBorrar' in request.values:
                accion = 'B'
            
            form = ProcessTaskForm(data={'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'date': fechaTarea, 'btn': accion})
        
        fTasks.close()
     
        return render_template("processtask.html", form=form)

    if form.btn.data == 'B':
        print('Borrar Registro')
        return redirect(url_for('index'))
    
    if form.btn.data == 'M':

        if form.validate():
            print('Modificar Registro')
            '''
            Crear fichero copia vacio en escritura
            Leer y copiar todos los registros desde tareas.dat a copia.dat hasta el anterior a modificar
            Grabar el nuevo registro con los datos del formulario
            Leer y copiar el resto de los registros hasta el final
            Cerrar los dos ficheros
            Borrar tareas.dat - Librería os
            Renombrar copia.dat a tareas.dat - Librería os
            '''

            original = open(DATOS, 'r')
            copia = open(COPIA, 'w')

            return redirect(url_for("index"))

        return render_template("processtask.html", form=form)
    



