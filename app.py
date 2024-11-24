from flask import Flask, jsonify, redirect, render_template, request, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from scripts.database import *
from scripts.constantes import *
from flask_session import Session
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required, logout_user
from models import User
from scripts.encrypt_url import *
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from flask_mail import Mail, Message 

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess = Session()

sess.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'doctor_login'
login_manager.init_app(app)

mail = Mail(app) # instantiate the mail class 

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'joanacarita@gmail.com'
app.config['MAIL_PASSWORD'] = 'MAISemelhor18!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

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
#FIX Key
key =  'AAAAAAAAAAAAAAAA' #16 char for AES128

def decrypt_ecb(enc, key):
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        return unpad(cipher.decrypt(enc),16)

@app.route("/formulario_koos")
def formulario_koos():
    return render_template("KOOS_Joelho.html", form_name = Form_KOOS_Joelho, radio_options = const_koos_12_crf(), users = read_users(current_user['id']))

@app.route("/patient_form_combo")
def patient_form_combo():
    return render_template("patient_form_combo.html", key = key, name = current_user['nome'], form_names = Form_Names, users = read_users(current_user['id']))


@app.route("/patient_form_selected", methods=['post'])
def patient_form_selected():
    data = request.form
    if data['formOptions'] == 'KOOS Joelho':
        return render_template("KOOS_Joelho.html", form_name = Form_KOOS_Joelho, radio_options = const_koos_12_crf(), users = read_users(current_user['id']), patientID = data['dropdown_patient_id'])
    else:
        return render_template("patient_form_combo.html", name = current_user['nome'], form_names = Form_Names, users = read_users(current_user['id']))

@app.route("/send_quest")
def send_quest():
    formOptions = request.args.get('chosen_form')
    dropdown_patient_id = request.args.get('chosen_patientID')

    test_url = url_for('patient_form_selected_url', chosen_form=formOptions, chosen_patientID=dropdown_patient_id, _external=True)

    return render_template("test_url.html", url = test_url)

@app.route("/test_url", methods=['post'])
def test_url():
    data = request.form

    msg = Message( 
                    'Hello', 
                    recipients = ['joanacarita@gmail.com'] 
                ) 
    msg.body = 'Hello Flask message sent from Flask-Mail'
    mail.send(msg) 

    return redirect(data['url_test'], code=302)

@app.route("/patient_form_selected_url")
def patient_form_selected_url():
    formOptions = request.args.get('chosen_form')
    dropdown_patient_id = request.args.get('chosen_patientID')

    decrypt_form_name = decrypt_ecb(formOptions, key).decode("utf-8", "ignore")
    decrypted_patient_id = decrypt_ecb(dropdown_patient_id, key).decode("utf-8", "ignore")

    if decrypt_form_name == 'KOOS Joelho':
        return render_template("KOOS_Joelho.html", form_name = decrypt_form_name, radio_options = const_koos_12_crf(), users = read_users(current_user['id']), patientID = decrypted_patient_id)
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

