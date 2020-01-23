from wtforms import IntegerField, StringField, ValidationError
from wtforms.validators import DataRequired

from app.models.user import User
from app.validators.base import BaseForm


class CreateUserForm(BaseForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])

    def validate_username(self, value):
        if User.get_by_id(self.username.data):
            raise ValidationError('User existed')


class ModifyUserForm(BaseForm):
    nickname = StringField()
    password = StringField()
    group = StringField()
    permission = IntegerField()
    status = StringField()


class SearchUserForm(BaseForm):
    nickname = StringField()
    group = StringField()
    permission = IntegerField()
    status = StringField()
