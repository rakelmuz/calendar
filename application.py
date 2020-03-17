# -- coding: utf-8 --
# schedulerdao import
from dao import schedulerdao
from flask import Flask, request, render_template
app = Flask(__name__)

#Acesso básico à página
@app.route("/")
def index():
    return render_template("index.html")

# GET E POST dos eventos
@app.route("/scheduler",methods=["GET","POST","PUT","DELETE"])
def scheduler():
    # Se a solicitação Get for recebida
    if request.method == 'GET':
        # No fullCalendar, o início e o final são registrados como parâmetros do formato aaaa-mm-dd.
        start = request.args.get('start')
        end = request.args.get('end')
       
        return schedulerdao.getEvento({'start':start , 'end' : end})

    #se for solicitado o post
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        allDay = request.form['allDay']

       
        schedule = {'title' : title, 'start' : start, 'end' : end, 'allDay' : allDay}
        # retorna evento
        return  schedulerdao.setEvento(schedule)

    #se for solicitado o delete
    if request.method == 'DELETE':
        id = request.form['id']
        return  schedulerdao.delEvento(id)

    #se for solicitado o put
    if request.method == 'PUT':
        schedule = request.form
        return schedulerdao.putEvento(schedule)


if __name__ =='__main__':
    app.run(debug=True)
