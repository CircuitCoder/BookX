from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from app import app,lm,db
from models import User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.before_request
def before_request():
	if current_user.is_authenticated():
		g.user = current_user
	else:
		g.user = None


@app.route('/')
def index():
	if g.user is not None and g.user.is_authenticated():
		return render_template("index.html", g = g)
		# if g.user.is_admin == True:
		# 	return redirect(url_for('administrator'))
		# else:
		# 	return redirect(url_for('user', username = g.user.username))
	
	return render_template("index.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if (user is not None and user.password == form.password.data and not user.is_ban):
			login_user(user)
			flash("Login successfully")
			return redirect(request.args.get('next') or url_for('index'))
			# if user.is_admin == True:
			# 	return redirect(request.args.get('next') or url_for('administrator'))
			# else:
			# 	return redirect(request.args.get('next') or url_for('user', username = user.username))
		form.password.data = ''
		flash("Login failed",'error')
		#session['remember_me'] = form.remember_me.data
	return render_template('login.html',
		g = g,
		form = form,
		islogin = True)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
	form = RegisterForm()

	if form.validate_on_submit():
		if form.password.data == form.password_again.data:
			user = User(
				username = form.username.data,
				password = form.password.data,
				mail = form.mail.data,
				tel = form.tel.data,
				school = form.school.data,
				address = form.address.data)
			try:
				db.session.add(user)
				db.session.commit()
			except:
				form.username.data = ''
				form.password.data = ''
				form.password_again.data = ''
				flash("The username has been used",'error')
				return render_template('register.html',
						g = g,
						form = form)
			login_user(user);
			flash("Register successfully")
			return redirect(url_for('index'))
		form.password.data = ''
		form.password_again.data = ''
		flash("Passwords are not the same",'error')

	return render_template('register.html',
		g = g,
		form = form)