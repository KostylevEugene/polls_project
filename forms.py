from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp         # проверяет наличие данных в форме

class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField('name', validators=[DataRequired(message='Could not be empty'),
                                            Length(min=4, message='Too short name. It must be more than 4 symbols'),
                                            Regexp(r'[a-zA-Z]+', message="Invalid username! Enter only \
                                                                            possible symbols a-z, 0-9")])

    email = StringField('email', validators=[DataRequired(message='Could not be empty'),
                                            Length(min=6, message='Too short email. It must be more than 6 symbols'),
                                            Regexp(r'[a-zA-Z]+', message="Invalid email! Enter only \
                                                                            possible symbols a-z, 0-9, @")])

                                                                            # TODO: изменить регекс для имейла

    password = PasswordField('password', validators=[DataRequired(message='Could not be empty'),
                                                    Length(min=6, max=64, message='Password length must be \
                                                                                    minimum %(min)d and maximum %(max)d symbols'),
                                                    Regexp(r'[a-zA-Z0-9/+!#$%^&*()`~]+', 
                                                            message='Password has permitted valid symbols - a-zA-Z0-9/+!#$%^&*()`~')])

    valid_password = PasswordField('valid_password', validators=[DataRequired(message='Could not be empty'),
                                                    Length(min=6, max=64, message='Password length must be \
                                                                                    minimum %(min)d and maximum %(max)d symbols'),
                                                    Regexp(r'[a-zA-Z0-9/+!#$%^&*()`~]+', 
                                                            message='Password has permitted valid symbols - a-zA-Z0-9/+!#$%^&*()`~')])

    register = SubmitField('Sign up')