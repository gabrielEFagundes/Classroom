from app import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import Register, Login, RegisterClass, NewActivity
from app.models import User, Class, Activities

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    data = Class.query.filter_by(teacher_id=current_user.id)

    classes = {'data' : data.all()}
    return render_template('index.html', user=current_user, classes=classes)

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
@login_required
def signClass():
    form = RegisterClass()

    if(form.validate_on_submit()):
        try:
            form.save()
            flash('Turma criada com sucesso!', 'success')
            return redirect(url_for('home'))
        
        except Exception as e:
            flash(str(e), 'danger')

    return render_template('new_class.html', form=form, user=current_user)

@app.route('/delete/class/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteClass(id):
    delete = Class.query.get(id)

    db.session.delete(delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/view/class/<int:id>', methods=['GET', 'POST'])
@login_required
def classPage(id):
    classroom = Class.query.get(id)
    data = Activities.query.filter_by(class_id=id)

    activities = {'data' : data.all()}

    return render_template('class_page.html', classroom=classroom, activities=activities)

@app.route('/view/class/<int:id>/new', methods=['GET', 'POST'])
def signActivity(id):
    form = NewActivity()

    if(form.validate_on_submit()):
        form.save()
        flash('Atividade salva com sucesso!', 'success')
        return redirect(url_for('classPage', id=id))
    
    return render_template('new_activity.html', form=form, classroom=id)