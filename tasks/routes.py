from tasks import app
from flask import render_template, request, redirect, url_for

import csv

@app.route("/")
def index():
    #leer el fichero csv
    fTasks = open('./data/tareas.dat', 'r')
    csvreader = csv.reader(fTasks, delimiter=',')
    datos = []

    for linea in csvreader:
        datos.append(linea)
   
    if datos != []:
        datos.sort(key=lambda x: x[2])

    return render_template("index.html", registros=datos)


@app.route("/newtask", methods=['GET', 'POST'])
def newtask():
    if request.method == 'GET':
        return render_template("task.html")
    
    if request.method == 'POST':
   
        fTasks = open('./data/tareas.dat', 'a')
        csvwriter = csv.writer(fTasks, delimiter=",", quotechar='"', lineterminator='\r')

        title = request.values.get('title')
        desc = request.values.get('desc')
        date = request.values.get('date')

        csvwriter.writerow([title, desc, date])

        fTasks.close

        return redirect(url_for("index"))

    print('method:', request.method)
    print('parametros:', request.values)
