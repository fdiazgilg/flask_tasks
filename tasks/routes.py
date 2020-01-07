from tasks import app
from flask import render_template, request, redirect, url_for
from tasks.forms import TaskForm

import csv

DATOS = './data/tareas.dat'

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
