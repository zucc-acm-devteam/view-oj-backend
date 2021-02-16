from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from app.validators.base import DateTimeForm


class CreateCompetitionForm(DateTimeForm):
    name = StringField(validators=[DataRequired(message='competition name cannot be empty')])
    link = StringField(validators=[DataRequired(message='competition link cannot be empty')])
    remark = StringField()


class ModifyCompetitionForm(DateTimeForm):
    name = StringField()
    link = StringField()
    remark = StringField()
