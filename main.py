import os
from flask import Flask, render_template,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import (StringField,SubmitField,BooleanField,DateTimeField,RadioField,SelectField,TextAreaField)
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


app.config['SECRET_KEY'] = 'anothersecretkey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,"data.sqlite")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Users(db.Model):
    __tablename__="users"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.Text)
    lastName = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
   

    def __init__(self,firstName,lastName,email,password):
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.password=password

    def __repr__(self):
        return f"the user is {self.firstName} {self.lastName}"

    @staticmethod
    def validate_login(email, password):
        user = Users.query.filter_by(email=email, password=password).first()
        return user is not None


class signUpForm(FlaskForm):
    firstName = StringField('What is your first name?:', validators=[DataRequired()])
    lastName = StringField('What is your last name?:', validators=[DataRequired()])
    email = StringField('What is your email address?:', validators=[DataRequired()])
    password = StringField('What is your password?:', validators=[DataRequired()])
    confirmPassword = StringField('Confirm your password:', validators=[DataRequired()])
    submit=SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        if Users.validate_login(email, password):
            session['email'] = email
            return redirect(url_for('secretpage'))
        else:
            return render_template('login.html', form=form, error="Invalid email or password.")
    return render_template('login.html', form=form)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/secretpage")
def secretpage():
    return render_template('secretpage.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = signUpForm()
    if form.validate_on_submit():
        if form.password.data == form.confirmPassword.data:
            new_user = Users(
                firstName=form.firstName.data,
                lastName=form.lastName.data,
                email=form.email.data,
                password=form.password.data
                
            )
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

                session['firstName']=form.firstName.data
                session['lastName']=form.lastName.data
                session['email']=form.email.data

                session.pop('password', None)
                session.pop('confirmPassword', None)
            return redirect(url_for('thankyou'))
        else:
            return render_template('signup.html',form=form,error="Passwords do not match.")

    return render_template('signup.html', form = form)






@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')