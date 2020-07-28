import json

from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.validators.base import BaseForm


class CreateCampForm(BaseForm):
    name = StringField(validators=[DataRequired(message='name required')])


class ModifyCampNameForm(BaseForm):
    name = StringField(validators=[DataRequired(message='name required')])


class CreateCourseForm(BaseForm):
    name = StringField(validators=[DataRequired(message='name required')])
    spider_username = StringField()
    spider_password = StringField()


class ModifyCourseForm(BaseForm):
    name = StringField(validators=[DataRequired(message='name required')])
    spider_username = StringField()
    spider_password = StringField()


class AppendContestForm(BaseForm):
    name = StringField(validators=[DataRequired(message='name required')])
    contest_cid = StringField(validators=[DataRequired(message='contest cid required')])


class ModifyCourseUsernameForm(BaseForm):
    username = StringField(validators=[DataRequired(message='username required')])
    oj_username = StringField()
