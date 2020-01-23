from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.models.oj import OJ
from app.validators.base import BaseForm


class OJUsernameForm(BaseForm):
    oj_id = IntegerField(validators=[DataRequired(message='OJ id cannot be empty')])
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])
    oj_username = StringField()

    def validate_oj_id(self, value):
        oj = OJ.get_by_id(self.oj_id.data)
        if not oj:
            raise ValidationError('OJ not exist')
        if oj.status != 1:
            raise ValidationError('OJ username not allow modify')


class SearchOJUsernameForm(BaseForm):
    oj_id = IntegerField()
    username = StringField()
