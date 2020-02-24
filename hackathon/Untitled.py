# %%
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
import requests

food_api_url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"

class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self,email):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            raise ValidationError("That Username is taken. Please choose a different one!")

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField(('Password'),validators=[DataRequired()])
    submit = SubmitField('Login')
    
class FoodForm(FlaskForm):
    name = StringField('Enter Food Name',validators=[DataRequired()])
    quantity = FloatField('Enter Quantity',validators=[DataRequired()])
    submit = SubmitField('Add Food')
    
    def valid_food(self):
        querystring = {"ingr":self.name.data}
        headers = {'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
                   'x-rapidapi-key': "08ec208f16msh8522ec90dda9930p140383jsn5c0e2158b994"}
        response = requests.request("GET", food_api_url, headers=headers, params=querystring)
        dc = response.json()
        if ("hints" in dc):
            if(len(dc["hints"])==0):
                raise ValidationError("Not a Valid Food Name")
        else:
                raise ValidationError("Not a Valid Food Name")
    
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
    foods = db.relationship('Food',backref='eater',lazy=True)
    def __repr__(self):
        return "email: {}, password: {},image: {}".format(self.email,self.password,self.image_file)
    def past_n(self,n):
        list_1 = Food.query.filter_by(user_id=self.id).all()
        a = {"protien":0,"carb":0,"calorie":0}
        for food in list_1:
            today = date.today()
            todayday=today.day
            food_day = food.food_date.day
            if(food_day==todayday-n+1):
                a["protien"]+=food.protien
                a["carb"]+=food.carb
                a["calorie"]+=food.calorie
        return a
    def past_week(self):
        list_1 = Food.query.filter_by(user_id=self.id).all()
        a = {"protien":0,"carb":0,"calorie":0}
        for food in list_1:
                a["protien"]+=food.protien
                a["carb"]+=food.carb
                a["calorie"]+=food.calorie
        return a
    
    def getWater(self):
        list_1 = Food.query.filter_by(user_id=self.id, food_name="water" or "Water" or "WATER").all()
        a = 0.0
        for food in list_1:
            a+=food.quantity
        return a
    
    
class Food(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    food_name= db.Column(db.String(20),unique = False, nullable= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_date = db.Column(db.Date, nullable=False,default=date.today())
    quantity = db.Column(db.Float, nullable=False, default =1)
    protien = db.Column(db.Float, nullable = False,default =0)
    calorie = db.Column(db.Float, nullable = False,default =0)
    carb = db.Column(db.Float, nullable = False,default =0)
    
    def __repr__(self):
        return "Name: {}, date: {},user_id :{} , protien:{}".format(self.food_name,self.food_date,self.user_id,self.protien)
    
    def getNutrients(self):
        querystring = {"ingr":self.food_name}
        headers = {'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com",
                   'x-rapidapi-key': "08ec208f16msh8522ec90dda9930p140383jsn5c0e2158b994"}
        response = requests.request("GET", food_api_url, headers=headers, params=querystring)
        dc = response.json()
        
        if('PROCNT' in dc['hints'][0]['food']['nutrients']):
            p1=dc['hints'][0]['food']['nutrients']['PROCNT']
            self.protien = float(p1)
        else:
            self.protien = 0.0
        
        if('CHOCDF' in dc['hints'][0]['food']['nutrients']):
            p2=dc['hints'][0]['food']['nutrients']['CHOCDF']
            self.carb = float(p2)
        else:
            self.carb=0.0
        
        if('ENERC_KCAL' in dc['hints'][0]['food']['nutrients']):
            p3=dc['hints'][0]['food']['nutrients']['ENERC_KCAL']
            self.calorie = float(p3)
        else:
            self.calorie = 0.0
        self.calorie *=(self.quantity)
        self.protien *=(self.quantity)
        self.carb *=(self.quantity)
        
        
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
            return render_template('dashboard.html',user = user,form = FoodForm(), date = date.today())
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


@app.route("/dashboard", methods = ['GET','POST'])
def dash():
    user = current_user
    form = FoodForm()
    
    if form.validate_on_submit():
        food_1 = Food(food_name=form.name.data, quantity=form.quantity.data, user_id=user.id)
        food_1.getNutrients()
        db.session.add(food_1)
        db.session.flush()
        db.session.commit()
        flash('Your Food Item has been successfully added!','success')
        return render_template("dashboard.html",user = user, form =form, date = date.today())
    flash('Not a valid food name.','danger')
    return render_template("dashboard.html",user = user, form= form, date= date.today())

@app.route("/display",methods =["GET"])
def display():
    user = current_user
    foods = Food.query.filter_by(user_id=user.id).all()
    return render_template("display.html",user=user,foods=foods)
    
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(email=form.email.data,password= hashed_pw)
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        flash('Your account has been created! Please log in through the Home Page!','success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# %%
