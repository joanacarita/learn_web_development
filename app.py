from flask import Flask, jsonify, render_template, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from scripts.database import *
from scripts.constantes import *
from flask_session import Session
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
from models import User
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()

sess.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'doctor_login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    #doctor_loged = read_doctors_by_id(id)
    user_entry = User.get(int(id))

    if not user_entry:
        return
    else:
        return user_entry


@app.route("/")
def home_page():
    return render_template("home.html", message = '')

######################## DOCTOR ###############################
@app.route("/doctor_login")
def doctor_login():
    return render_template("doctor_login.html")

@app.route("/doctor_login_completed", methods=['post'])
def doctor_login_completed():
    data = request.form
    
    doctor_id = read_doctors_by_email(data['email'])
    doctor = User.get(doctor_id)

    # check if the doctor actually exists
    # take the doctor-supplied password, hash it, and compare it to the hashed password in the database
    if not doctor or not check_password_hash(doctor['password'], data['password']):
        flash('Please check your login details and try again.')
        return render_template("doctor_login.html") # if the user doesn't exist or password is wrong, reload the page
    else:
        user = User(doctor['id'], doctor['email'], doctor['numero_ordem'], doctor['nome'], doctor['apelido'])
        login_user(user, remember=True)#data['remember']
    
    # if the above check passes, then we know the user has the right credentials
    
    return render_template("doctor_home_page_protected.html", name=current_user.nome)

@app.route('/doctor_home_page_protected')
@login_required
def doctor_home_page_protected(doctor_name):
    return render_template('doctor_home_page_protected.html', name=doctor_name)

@app.route('/doctor_logout')
def doctor_logout():
    logout_user()
    return render_template("home.html", message = 'Logged out') 

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
    write_patient_to_db(data, current_user['id'])
    return render_template('patient_register_successfull.html', 
         application=data)

######################## FORMS ###############################

@app.route("/formulario_koos")
def formulario_koos():
    return render_template("KOOS_Joelho.html", form_name = Form_KOOS_Joelho, radio_options = const_koos_12_crf(), users = read_users(current_user['id']))

@app.route("/patient_form_combo")
def patient_form_combo():
    return render_template("patient_form_combo.html", name = current_user['nome'], form_names = Form_Names, users = read_users(current_user['id']))

@app.route("/patient_form_selected", methods=['post'])
def patient_form_selected():
    data = request.form
    if data['formOptions'] == 'KOOS Joelho':
        return render_template("KOOS_Joelho.html", form_name = Form_KOOS_Joelho, radio_options = const_koos_12_crf(), users = read_users(current_user['id']), patientID = data['dropdown_patient_id'])
    else:
        return render_template("patient_form_combo.html", name = current_user['nome'], form_names = Form_Names, users = read_users(current_user['id']))


@app.route("/patient_form_selected_url")
def patient_form_selected_url():
    formOptions = request.args.get('formOptions')
    dropdown_patient_id = request.args.get('dropdown_patient_id')
    if formOptions == 'KOOS Joelho':
        return render_template("KOOS_Joelho.html", form_name = formOptions, radio_options = const_koos_12_crf(), users = read_users(current_user['id']), patientID = dropdown_patient_id)
    else:
        return render_template("patient_form_combo.html", name = current_user['nome'], form_names = Form_Names, users = read_users(current_user['id']))


@app.route("/guardar_quest", methods=['post'])
def guardarQuest():
    data = request.form
    write_respostas_quest_to_db(data)
    return render_template('questionario_completed.html', 
         application=data)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)

