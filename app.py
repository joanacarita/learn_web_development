from flask import Flask, jsonify, render_template, request
from scripts.database import *
from scripts.constantes import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html", radio_options = const_koos_12_crf(), users = read_users())

@app.route("/signincomplete", methods=['post'])
def signin():
    data = request.form
    write_medico_to_db(data)
    return render_template('signin_successfull.html', 
         application=data)

@app.route("/guardar_quest", methods=['post'])
def guardarQuest():
    data = request.form
    write_respostas_quest_to_db(data)
    return render_template('questionario_completed.html', 
         application=data)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)

