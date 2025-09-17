from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired

from app import db, bcrypt
from app.models import User, Class, Activities

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if(user):
            raise Exception('Email já está em uso!')
        
    def save(self):
        password = bcrypt.generate_password_hash(self.password.data.encode('utf-8'))
        new_user = User(
            name=self.username.data,
            email=self.email.data,
            password=password.decode('utf-8')
        )
        db.session.add(new_user)
        db.session.commit()

        return new_user
    
class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        
        if(user):
            if(bcrypt.check_password_hash(user.password, self.password.data.encode('utf-8'))):
                return user

            else:
                raise Exception('Senha incorreta!')
            
        else:
            raise Exception('Usuário não encontrado!')
        
class RegisterClass(FlaskForm):
    name = StringField('Class Name', validators=[DataRequired()])
    teacher_id = IntegerField('Teacher ID', validators=[DataRequired()])
    submit = SubmitField('Create Class')

    def save(self):
        new_class = Class(
            name=self.name.data,
            teacher_id=self.teacher_id.data
        )

        db.session.add(new_class)
        db.session.commit()

        return new_class
    
class NewActivity(FlaskForm):
    title = StringField("Activity's Title", validators=[DataRequired()])
    description = StringField("Activity's Description", validators=[DataRequired()])
    class_id = IntegerField("Class' ID", validators=[DataRequired()])
    submit = SubmitField('Send Activity')

    def save(self):
        new_activity = Activities(
            title=self.title.data,
            description=self.description.data,
            class_id=self.class_id.data
        )

        db.session.add(new_activity)
        db.session.commit()

        return new_activity