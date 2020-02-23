# %%
from flask import Flask, render_template,url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That Username is taken. Please choose a different one!")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField(('Password'),validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
app = Flask(__name__)
app.config['SECRET_KEY'] = b'\xc5!\xddk\xd7\x08\x85\x973H\x7f\xc5D}\xf5\x92ZMW\xd0g(\x01\x03'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='#')
    def __repr__(self):
        return{"email: {}, password: {},image: {}".format(self.email,self.password,self.image_file)}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods =["GET","POST"])
@app.route("/home", methods =["GET","POST"])
def home():
    form = LoginForm()
    if(form.validate_on_submit()):
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)
            flash("Logged in as {}".format(user.email),'success')
            return render_template('dashboard.html',user=user)
        flash("Log in Unsuccessful! Please check username and password",'danger')
    return render_template('home.html',form = form)
    
@app.route("/about")
def about():
    return("About")

@app.route("/logout")
def logout():
    logout_user()
    flash("You have successfully logged out!" , 'success')
    return redirect(url_for('home'))

@app.route("/dashboard")
def dash():
    user = user
    return render_template("dashboard.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(email=form.email.data,password= hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to Log in','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# %%
user_1=User.query.all()
for user in user_1:
    print(user.email)