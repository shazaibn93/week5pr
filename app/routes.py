from app import app
from .forms import PokeForm, LoginForm, RegisterForm
from .models import User
from flask_login import login_user, current_user, logout_user, login_required

from flask import Flask, render_template, request, flash, redirect, url_for
import requests

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/team', methods=['GET','POST'])
def team():
    form=PokeForm()
    if request.method == 'POST' and form.validate_on_submit():
        # contact the api and get the name of the pokemon from the form
        poke = request.form.get('poke').lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{poke}"
        response = requests.get(url)
        if response.ok:
            poke_dict={
                'name':response.json()['forms'][0]['name'],
                 "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],
                "ability_2":response.json()['abilities'][1]['ability']['name'],
                "sprite": response.json()['sprites']['front_shiny']
            }
            
            return render_template('team.html.j2', form=form, mpoke = poke_dict )
        else:
            error_string = "Houston We Have a Problem"
            return render_template('team.html.j2', form=form, error = error_string)
    return render_template('team.html.j2', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        #We will do the login stuff here
        email = request.form.get('email').lower()
        password = request.form.get('password')
        U = User.query.filter_by(email=email).first() #Left is column, right is variable
        if U and U.check_hashed_password(password):
            login_user(U)
            flash('Welcome to Fakebook', 'success')
            return redirect(url_for('index'))
        flash("Incorrect Email Password Combo")
        return render_template('login.html.j2', form = form)
    return render_template('login.html.j2', form = form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        return redirect(url_for('login'))



@app.route('/register',methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        #Create a new user 
        try:
            new_user_data = {
                "first_name":form.first_name.data.title(),
                "last_name":form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            #creating an empty user 
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash("We ran into an error ",'danger')
            #Error Return
            return render_template('register.html.j2', form=form)
        # If it worked
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    #Get Return
    return render_template('register.html.j2', form=form)