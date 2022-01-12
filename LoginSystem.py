from flask import Flask, g, request, render_template, redirect, session, url_for
import requests
from json import loads as deserialize

app = Flask(__name__, static_url_path='')
app.secret_key = "thisisasecretkey"
url = "http://127.0.0.1:5001"

@app.route("/")
def LoginPage():
    if "token" in session:
        token = session["token"]
        return redirect("/dashboard")
    else:
        return render_template("loginPage.html")

@app.route("/", methods = ["GET","POST"])
def user_login():
    if request.method =="POST":
        reqEmailLog = request.form['email']
        reqPassLog = request.form['password']
        user_CRED = {
                'email':reqEmailLog,
                'password':reqPassLog,
                }
        json_data = requests.post(url + '/api/login', json = user_CRED, verify=False)
        print(json_data.content)
        des_cont = deserialize(json_data.content)
        session["token"]= (des_cont["token"])
        return redirect("/dashboard")

@app.route("/register", methods = ["GET", "POST"])
def user_register():
    if request.method == "POST":
        regEmail = request.form['email']
        regPass = request.form['password']
        user_CRED = {
            'email':regEmail,
            'password':regPass
            }
        requests.post(url + '/api/register', json = user_CRED, verify=False)
        return redirect("/")
    return render_template("register.html")

@app.route("/dashboard", methods = ["GET", "POST"])
def dashboard():
    if "token" in session:
        return render_template("dashboard.html")
    else:
        return redirect("/")
    
@app.route("/logout")
def logout():
    session.pop("token", None)
    return redirect("/")

if __name__== "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)