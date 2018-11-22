from flask_wtf import Form
from wtforms import PasswordField, TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import datetime
import calendar



#con = pymysql.connect(db='BankAccount', password='independence', user='Learn')



#cursor = con.cursor()

class SignupForm(FlaskForm):
    name = StringField("Username",[validators.DataRequired()])
    email = StringField("Email",[validators.DataRequired(),
    validators.Email()])
    password = PasswordField("Password",[validators.DataRequired()])
    submit = SubmitField('Register')





