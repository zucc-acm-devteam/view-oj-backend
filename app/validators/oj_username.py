from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.models.oj import OJ
from app.models.oj_username import OJUsername
from app.validators.base import BaseForm


class CreateOJUsernameForm(BaseForm):
    oj_id = IntegerField(validators=[DataRequired(message='OJ id cannot be empty')])
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    oj_username = StringField(validators=[DataRequired(message='OJUsername cannot be empty')])
    oj_password = StringField()
    is_team_account = IntegerField()
    is_child_account = IntegerField()

    def validate_oj_id(self, value):
        oj = OJ.get_by_id(self.oj_id.data)
        if not oj:
            raise ValidationError('OJ not exist')
        if oj.status != 1:
            raise ValidationError('OJ username not allow modify')

    def validate_is_team_account(self, value):
        if self.is_team_account.data is None:
            self.is_team_account.data = False
        oj = OJ.get_by_id(self.oj_id.data)
        if not oj.allow_team and self.is_team_account.data:
            raise ValidationError('Team account not allowed')

    def validate_is_child_account(self, value):
        if self.is_child_account.data is None:
            self.is_child_account.data = False
        oj = OJ.get_by_id(self.oj_id.data)
        if not oj.allow_child_account and self.is_child_account.data:
            raise ValidationError('Child account not allowed')


class ModifyOJUsernameForm(BaseForm):
    oj_username_id = IntegerField(validators=[DataRequired(message='OJUsername id cannot be empty')])
    oj_username = StringField(validators=[DataRequired(message='OJUsername cannot be empty')])
    oj_password = StringField()

    def validate_oj_username_id(self, value):
        oju = OJUsername.get_by_id(self.oj_username_id.data)
        if not oju:
            raise ValidationError('OJUsername not exist')


class DeleteOJUsernameForm(BaseForm):
    oj_id = IntegerField(validators=[DataRequired(message='OJ id cannot be empty')])
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    oj_username = StringField(validators=[DataRequired(message='OJUsername cannot be empty')])

    def validate_oj_id(self, value):
        oj = OJ.get_by_id(self.oj_id.data)
        if not oj:
            raise ValidationError('OJ not exist')
        if oj.status != 1:
            raise ValidationError('OJ username not allow modify')
