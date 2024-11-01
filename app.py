from flask import Flask, jsonify, render_template, request
from scripts.database import *
from scripts.constantes import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

######################## DOCTOR ###############################
@app.route("/doctor_signin")
def doctor_signin():
    return render_template("doctor_signin.html")

@app.route("/doctor_signin_complete", methods=['post'])
def doctor_signin_complete():
    data = request.form
    write_doctor_to_db(data)
    return render_template('doctor_signin_successfull.html', 
         application=data)

######################## PATIENT ###############################

@app.route("/patient_register")
def patient_register():
    return render_template("patient_register.html")

@app.route("/patient_register_complete", methods=['post'])
def patient_register_complete():
    data = request.form
    write_patient_to_db(data)
    return render_template('patient_register_successfull.html', 
         application=data)

######################## FORMS ###############################

@app.route("/formulario_koos")
def formulario_koos():
    return render_template("KOOS_Joelho.html", radio_options = const_koos_12_crf(), users = read_users())

@app.route("/guardar_quest", methods=['post'])
def guardarQuest():
    data = request.form
    write_respostas_quest_to_db(data)
    return render_template('questionario_completed.html', 
         application=data)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)

