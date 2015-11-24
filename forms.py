from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email, Length, EqualTo)
from models import User

def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('A user with that username already exists! Please choose another username')

def email_exists(form, field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('A user with that email already exists! Please enter another email address')

class RegisterForm(Form): #Registration form validation
	username = StringField(
		'Username',
		validators=[
			DataRequired(),
			Regexp(r'^[a-zA-Z0-9_]+$#', message=("Your username should be one word")
			),
				name_exists
			])
				
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists
			])
	
	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo('password2', message='Your passwords must match')
			])
	password2 = PasswordField(
		'Confirm Password',
			validators=[DataRequired()]
			)

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])