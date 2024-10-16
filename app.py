from flask import Flask, jsonify, render_template, request
from database import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/signincomplete", methods=['post'])
def signin():
    data = request.form
    write_medico_to_db(data)
    return render_template('signin_successfull.html', 
         application=data)

@app.route("/apply", methods=['post'])
def apply_to_job():
    data = request.form
    return jsonify(data)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug = True)

