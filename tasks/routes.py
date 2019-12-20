from tasks import app
from flask import render_template, request

import csv

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("task.html")
    
    fDatos = open('./data/tareas.dat', 'w')
    csvwriter = csv.writer(fDatos, delimiter=",", quotechar='"')

    title = request.values.get('title')
    desc = request.values.get('desc')
    date = request.values.get('date')

    csvwriter.writerow([title, desc, date])

    fDatos.close

    return render_template("task.html")


    print('method:', request.method)
    print('parametros:', request.values)



'''
    recuperar parametros
    abrir fichero
    añadir registros
    devolver respuesta todo correcto
'''