from wtforms import StringField
from wtforms.validators import DataRequired

from app.validators.base import BaseForm


class LoginForm(BaseForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    password = StringField(validators=[DataRequired(message='Password cannot be empty')])
