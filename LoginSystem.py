import pyotp
import sqlite3 #Database that will be used
import hashlib
import uuid
from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)
db_name = 'UserCred.db'

@app.route("/")
def homepage():
    return render_template("homepage.html")

def verify_cred(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_CRED WHERE USERNAME = '{0}'".format(username)
    c.execute(query)
    records = c.fetchone()
    conn.close()
    if not records:
        return False
    return records[0] == password

@app.route("/", methods = ["GET","POST"])
def user_login():
    reqUserLog = request.form['Username']
    reqPassLog = request.form['Password']
    error = None
    if request.method == 'POST':
        if verify_cred(reqUserLog, reqPassLog):
            error = 'login success'
        else:
            error = 'Invalid username/password'
    else:
        error = 'Invalid Method'
    return error

@app.route("/register", methods = ["GET", "POST"])
def user_register():
    if request.method == "POST":
        reqUser = request.form['Username']
        reqPass = request.form['Password']
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS USER_CRED(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL);''')
        conn.commit()
        try:
            c.execute("INSERT INTO USER_CRED (USERNAME,PASSWORD)" "VALUES('{0}', '{1}')".format(reqUser,reqPass))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username has been registered."
        print('username: ', reqUser, 'password: ', reqPass)
    return render_template("Register.html")

if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)