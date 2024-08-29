from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import sqlalchemy as sa
from sqlalchemy import Integer, String
from APIkeys import polygonAPIkey
from polygon import RESTClient
import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLi_app = Flask(__name__)
SQLi_app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'SQLi_app.db')

db = SQLAlchemy(SQLi_app)
ma = Marshmallow(SQLi_app)

client = RESTClient(polygonAPIkey)

class SQLiData(db.Model):
    __tablename__ = 'SQLi_table'
    id = db.Column(Integer, primary_key = True)
    name = db.Column(String, nullable = True)
    email = db.Column(String, nullable = True)
    phoneNr = db.Column(Integer, nullable = True)
    username = db.Column(Integer, nullable = False)
    password = db.Column(String, nullable = False)

    def __init__(self, name, email, phoneNr, username, password) -> None:
        super(SQLiData, self).__init__()
        self.name = name
        self.email = email
        self.phoneNr = phoneNr
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return '<SQLiData %r>' % self.name
    

class SQLiDataSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'phoneNr', 'username', 'password')

multiple_SQLi_data_schema = SQLiDataSchema(many = True)

with SQLi_app.app_context():
    db.create_all()


    #Just manual adding/deleting of users when code is run
    '''
    user = SQLiData(
                name="",
                email="",
                phoneNr=,
                username = "",
                password = ""
                )
    db.session.add(user)
    db.session.commit()
    '''

    
    '''
    for i in range(5):
        id = i
        user = db.get_or_404(SQLiData, id)
        db.session.delete(user)
        db.session.commit()
        print("Deleted user", i)
    '''
    '''
    result = db.session.execute(db.select(SQLiData).order_by(SQLiData.name)).scalars()

    for i in result:
        print(i.id, i.name, i.email, i.phoneNr, "Username: ", i.username, "password: ", i.password)
    '''

@SQLi_app.route("/", methods=["GET", "POST"])
def user_list():
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in the database
        query = f"SELECT * FROM SQLi_table WHERE username = '{username}' AND password = '{password}'"
        user = db.session.execute(sa.text(query)).fetchone()

        if user:
            # If the user exists, retrieve all users (for demonstration purposes)
            users = db.session.execute(db.select(SQLiData).order_by(SQLiData.name)).scalars()
            return render_template("user/list.html", users=users, login_success=True)
        else:
            # If the user doesn't exist, return to the login page with an error
            return render_template("user/list.html", error="Invalid username or password.")

    # If it's a GET request, just render the login form
    return render_template("user/list.html", users=None)
