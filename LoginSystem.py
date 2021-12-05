import sqlite3 #Database that will be used
from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__, static_url_path='')

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/", methods = ["GET","POST"])
def user_login():
    reqUserLog = request.form['Username']
    reqPassLog = request.form['Password']
    json_data = requests.get("http://10.0.2.15:5000/users/" + reqUserLog).json()
    print(json_data)
    if json_data['user_USERNAME'] == reqUserLog and json_data['user_PASS'] == reqPassLog:
        return redirect("/LoggendIn")
    else:
        return f"Invalid Username and Password."

@app.route("/register", methods = ["GET", "POST"])
def user_register():
    if request.method == "POST":
        regUSERNAME = request.form['Username']
        regFNAME = request.form['Firstname']
        regLNAME = request.form['Lastname']
        regPass = request.form['Password']

        json_data = requests.get("http://10.0.2.15:5000/users/"+regUSERNAME, verify=False).json()
        print(len(json_data))
        if len(json_data) > 0:
            return f"User already exists"
        else:
            user_CRED = {
                'user_USERNAME':regUSERNAME,
                'user_FNAME':regFNAME,
                'user_LNAME':regLNAME,
                'user_PASS':regPass
                }
            requests.post('http://10.0.2.15:5000/users', json = user_CRED, verify=False)
            return redirect("/")

    return render_template("Register.html")

@app.route('/Monitoring', methods = ['GET', 'POST'])
def monitoring():
    return render_template('Monitoring.html')

@app.route('/LoggendIn', methods = ['GET', 'POST'])
def introduction():
    return render_template('LoggendIn.html')

@app.route('/About', methods = ['GET', 'POST'])
def about():
    return render_template('About.html')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)