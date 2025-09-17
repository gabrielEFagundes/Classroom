from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import Register, Login, RegisterClass
from app.models import User, Class

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    
    if(form.validate_on_submit()):
        try:
            user = form.login()
            login_user(user, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        
        except Exception as e:
            flash(str(e), 'danger')
    
    return render_template('login_page.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()

    if(form.validate_on_submit()):
        try:
            user = form.save()
            login_user(user, remember=True)
            flash('Usuário cadastrado com sucesso!', 'success')
            return redirect(url_for('home'))
        
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('signin_page.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/new/class', methods=['GET', 'POST'])
def signClass():
    form = RegisterClass()

    if(form.validate_on_submit()):
        try:
            new_class = form.save()
            flash('Turma criada com sucesso!', 'success')
            return redirect(url_for('home'))
        
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('new_class.html', form=form)