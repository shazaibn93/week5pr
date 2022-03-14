from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User

class PokeForm(FlaskForm):
    #field name = DataTypeField('LABEL', validators=[LIST OF validators])
    poke= StringField('Pokemon',validators = [DataRequired()])
    submit = SubmitField('Search')


class LoginForm(FlaskForm):
    #field name = DataTypeField('LABEL', validators=[LIST OF validators])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    email = StringField('Email Address', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators = [DataRequired(), EqualTo('password', message = 'Passwords must match')])
    submit = SubmitField('Register')
    #validate_FIELDNAME
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        
        if same_email_user:
            raise ValidationError('This email is already in use')