import pyotp
import sqlite3 #Database that will be used
import hashlib
import uuid
from flask import Flask, request, render_template, redirect
import os

#currentlocation = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

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

@app.route("/register", methods = ["GET", "POST"])
def registerpage():
    if request.method == "POST":
        dUN = request.form["DUsername"]
        dPW = request.form['DPassword']
        Uemail = request.form['Emailuser']
        sqlconnection = sqlite3.connection(currentlocation + "\Login.db")
        cursor = sqlconnection.cursor()
        query1 = "INSERT INTO Users VALUES('{u}','{p}','{e}')".format(u = dUN, p = dPW, e = Uemail)
        cursor.execute(query1)
        sqlconnection.commit()
        return redirect("/")
    return render_template("Register.html")

if __name__== "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)