from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm, ProcessTaskForm

import csv, sqlite3, os
from datetime import date

DATOS = './data/tareas.dat'
COPIA = './data/copia.dat'
BASE_DATOS = './data.tasks.db'


def openFiles(DATOS, COPIA):
    original = open(DATOS, 'r')
    copia = open(COPIA, 'w')

    return original, copia


def closeFiles(original, copia):
    original.close()
    copia.close()


def renameFiles(DATOS, COPIA):
    os.remove(DATOS)
    os.rename(COPIA, DATOS)



@app.route("/")
def index():
    #leer el fichero csv
    fTasks = open(DATOS, 'r')
    csvreader = csv.reader(fTasks, delimiter=',')
    datos = []

    for linea in csvreader:
        datos.append(linea)

    fTasks.close()
    
    '''
    if datos != []:
        datos.sort(key=lambda x: x[2])
    '''

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
        fx = request.values.get('fx')

        csvwriter.writerow([title, desc, fx])

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

        
        ix = request.values.get('ix')
        if ix:
            ix = int(ix)
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
                
                form = ProcessTaskForm(data={'ix': ix, 'title': registroAct[0], 'description': registroAct[1], 'fx': fechaTarea, 'btn': accion})
            
            fTasks.close()
        
            return render_template("processtask.html", form=form)
        else:
            return redirect(url_for('index'))


    if form.btn.data == 'B':

        original, copia = openFiles(DATOS, COPIA)
        csvreader = csv.reader(original, delimiter=",", quotechar='"')

        ix = int(request.values.get('ix'))
        for ilinea, linea in enumerate(csvreader, start=1):
            csvwriter = csv.writer(copia, delimiter=",", quotechar='"', lineterminator='\r')
        
            if ilinea == ix:
                pass

            else:
                title = linea[0]
                desc = linea[1]
                fx = linea[2]

                csvwriter.writerow([title, desc, fx])

        closeFiles(original, copia)
        renameFiles(DATOS, COPIA)

        return redirect(url_for('index'))
    
    if form.btn.data == 'M':

        if form.validate():
            
            original, copia = openFiles(DATOS, COPIA)
            csvreader = csv.reader(original, delimiter=",", quotechar='"')

            ix = int(request.values.get('ix'))
            for ilinea, linea in enumerate(csvreader, start=1):
                csvwriter = csv.writer(copia, delimiter=",", quotechar='"', lineterminator='\r')
           
                if ilinea == ix:
                    title = request.values.get('title')
                    desc = request.values.get('description')
                    fx = request.values.get('fx')

                    csvwriter.writerow([title, desc, fx])

                else:
                    title = linea[0]
                    desc = linea[1]
                    fx = linea[2]

                    csvwriter.writerow([title, desc, fx])

            closeFiles(original, copia)
            renameFiles(DATOS, COPIA)

            return redirect(url_for("index"))

        return render_template("processtask.html", form=form)