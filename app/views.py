"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from flask.ext.wtf import Form 
from wtforms.fields import TextField,FileField,StringField # other fields include PasswordField 
from wtforms.validators import Required, Email
from app.models import Myprofile
from app.forms import LoginForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app import oid, lm
from flask.ext.login import login_user,current_user,login_required,login_url
from flask.ext.login import LoginManager

from wtforms.validators import Required
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired
from werkzeug import secure_filename
import os
import random
from random import randrange, randint


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(userid):
    return Myprofile.query.get(userid)

class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])
     email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
     
     image = FileField('Image', validators=[Required(), Email()])


@app.before_request
def before_request():
    g.user = current_user
    
###
# Routing for your application.
###
# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     print app.config['OPENID_PROVIDERS']
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#     return render_template('login.html', 
#                           title='Sign In',
#                           form=form,
#                           providers=app.config['OPENID_PROVIDERS'])
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')
    
    
@app.route("/login/", methods=["GET", "POST"])    
def login():
    form = LoginForm()
    if request.method == "POST":
        pass
    # change this to actually validate the user
    if form.validate_on_submit():
        # login and validate the user...
        email = request.form['email']
        password = request.form['password']
        
        user = Myprofile.query.filter_by(email=email, password=password).first()
        
        user = load_user("1")
        login_user(user)
        #flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("home"))
    return render_template("login.html", form=form)

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    if request.method == 'POST':
        id = random.randint(1000000, 1099999)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        nickname = request.form['nickname']
        email = request.form['email']
        password = request.form['password']
                
        file = request.files['image']
        image = secure_filename(file.filename)
        file.save(os.path.join("pics", image))


        # write the information to the database
        newprofile = Myprofile(id=id, first_name=first_name,
                               last_name=last_name, nickname=nickname, email=email, password =password, image= image)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database".format(request.form['first_name'],
                                             request.form['last_name'])

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    all_users = db.session.query(Myprofile).all()
    users = []
    for user in all_users:
        users.append({"id": user.id, "email":user.email, "password":user.password})
        if request.headers['Content-Type']=='application/json' or request.method == 'POST':
            return jsonify(users)
    return render_template('profile_list.html',
                            users=users)

@app.route('/profile/<int:id>/')
def profile_view(id):
    profile = Myprofile.query.get(id)
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
