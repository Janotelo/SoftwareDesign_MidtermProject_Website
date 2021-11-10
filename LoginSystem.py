import pyotp
import sqlite3 #Database that will be used
import hashlib
import uuid
from flask import Flask, request, render_template, redirect
import os

#currentlocation = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
db_name = 'User.db'

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/", methods = ["POST"])
def checklogin():
    UN = request.form['Username']
    PW = request.form['Password']

    sqlconnection = sqlite3.connection(currentlocation + "\Login.db")
    cursor = sqlconnection.cursor()
    query1 = "SELECT Username, Password From Users WHERE Usernmae = '{un}' AND Password = '{pw}'".format(un = UN, pw = PW)

    rows = cursor.execute(query1)
    rows = rows.fetchall()
    if len(rows) == 1:
        return render_template("LoggedIn.html")
    else:
        return render_template("/register")

def checkloginv2():
    UN = request.form['Username']
    PW = request.form['Password']

    sqlconnection = sqlite3.connection(currentlocation + "\Login.db")
    cursor = sqlconnection.cursor()
    query1 = "SELECT Username, Password From Users WHERE Usernmae = '{un}' AND Password = '{pw}'".format(un = UN, pw = PW)

    rows = cursor.execute(query1)
    rows = rows.fetchall()
    if len(rows) == 1:
        return render_template("LoggedIn.html")
    else:
        return render_template("/register")    

@app.route("/register", methods = ["GET", "POST"])
def registerpagev2():
    reqUser = request.form['username']
    reqPass = request.form['password']
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_CRED(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL);''')
    conn.commit()
    try:
        c.execute("INSERT INTO USER_CRED (USERNAME,PASSWORD)" "VALUES('{0}', '{1}')".format(request.form['username'],request.form['password]))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Username has been registered."
    print('username: ', request.form['username'], 'password: ', request.form('password'))
    return "signup success"

if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)