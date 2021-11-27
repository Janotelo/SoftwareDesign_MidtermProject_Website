from flask import Flask, jsonify, request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlite3

app = Flask(__name__, static_url_path='')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserCred_Prac.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)

# conn = sqlite3.connect('UserCred_Prac.sqlite') # call database here
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS User_table(
#     user_ID TEXT PRIMARY KEY NOT NULL, 
#     user_USERNAME TEXT NOT NULL,
#     user_FNAME TEXT NOT NULL,
#     user_LNAME TEXT NOT NULL,
#     user_PASS TEXT NOT NULL);''')
# conn.commit()

class User(db.Model):
    __tablename__= "User_table"
    user_ID = db.Column(db.String(50), primary_key=True)
    user_USERNAME = db.Column(db.String(50))
    user_FNAME = db.Column(db.String(50))
    user_LNAME = db.Column(db.String(50))
    user_PASS = db.Column(db.String(50))

    def __init__(self,user_ID,user_USERNAME,user_FNAME,user_LNAME,user_PASS):
        self.user_ID = user_ID
        self.user_USERNAME = user_USERNAME
        self.user_FNAME = user_FNAME
        self.user_LNAME = user_LNAME
        self.user_PASS = user_PASS

class UserSchema(ma.Schema):
    class Meta:
        fields = ("user_ID", "user_USERNAME", "user_FNAME", "user_LNAME", "user_PASS")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def create_user():
    user_ID = request.json.get('user_ID')
    user_USERNAME = request.json.get('user_USERNAME')
    user_FNAME = request.json.get('user_FNAME')
    user_LNAME = request.json.get('user_LNAME')
    user_PASS = request.json.get('user_PASS')
    new_user = User(user_ID,user_USERNAME,user_FNAME,user_LNAME,user_PASS)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/users', methods=['GET'])
def read_all():
    users = User.query.all()
    result = users_schema.dump(users)
    return users_schema.jsonify(result).data

@app.route('/users/<user_ID>', methods=['GET'])
def read_user(user_ID):
    User_table = User.query.get(user_ID)
    result = user_schema.dump(User_table)
    return user_schema.jsonify(result)

@app.route('/users/<user_ID>', methods=['PUT'])
def update_student(user_ID):
    User_table = User.query.get(user_ID)

    user_ID = request.json.get('user_ID')
    user_USERNAME = request.json.get('user_USERNAME')
    user_FNAME = request.json.get('user_FNAME')
    user_LNAME = request.json.get('user_LNAME')

    User_table.user_USERNAME = user_USERNAME
    User_table.user_FNAME = user_FNAME
    User_table.user_LNAME = user_LNAME

    db.session.commit()
    return user_schema.jsonify(User_table)

@app.route('/users/<user_ID>', methods=['DELETE'])
def delete_user(user_ID):
    User_table = User.query.get(user_ID)
    db.session.delete(User_table)
    db.session.commit()

    return user_schema.jsonify(User_table)

if __name__== "__main__":
    db.create_all()
    app.run(host='127.0.0.5', port=5050, debug=True)