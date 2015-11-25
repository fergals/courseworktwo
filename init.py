from flask import Flask, g, render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user

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
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close() #close the database connection after each request
    return response
	
@app.route('/')
def index():
    allposts = models.Post.select().limit(100)
    return render_template('allposts.html', allposts=allposts)

@app.route('/register/', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit(): #run registration form validation
        flash("You have registered successfully", "success") #use success flash message
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('registration.html', form=form)

	
@app.route('/login/', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if user.password == form.password.data:
                login_user(user) #create login session
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))

@app.route('/newpost/', methods=('GET', 'POST'))
@login_required #user must be logged in to post msg
def post():
	form = forms.PostForm()
	if form.validate_on_submit():
		models.Post.create(user=g.user._get_current_object(),
						   content=form.content.data.strip())
		flash("Msg has been posted", "success")
		return redirect(url_for('index'))
	return render_template('postmsg.html', form=form)
		
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, host=HOST, port=PORT)