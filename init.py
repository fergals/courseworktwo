from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask.ext.login import LoginManager

import forms
import models

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'sdhfjorytjhsdfgbnksadghjkdefg'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE #connect to the database before each request
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close() #close the database connection after each request
    return response

@app.route('/register/', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit(): #run form validation
        flash("You have registered successfully", "success") #use success flash message
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)

@app.route('/')
def index():
    return 'Homepage is working... kinda...'

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='fergal',
            email='test@test.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)