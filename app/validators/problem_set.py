import json
import re

from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.validators.base import NotRequiredDateTimeForm


class CreateProblemSetForm(NotRequiredDateTimeForm):
    name = StringField(validators=[DataRequired(message='Problem set name cannot be empty')])
    problem_list = StringField(validators=[DataRequired(message='Problem list cannot be empty')])

    def validate_problem_list(self, value):
        try:
            self.problem_list.data = json.loads(self.problem_list.data)
            if not isinstance(self.problem_list.data, list):
                raise Exception()
        except Exception:
            raise ValidationError('Problem list must be list')
        for i in self.problem_list.data:
            if re.match('[a-z_]+-.+', i['problem']) is None:
                raise ValidationError('Problem format error')


class ModifyProblemSetForm(NotRequiredDateTimeForm):
    name = StringField()
    problem_list = StringField()

    def validate_problem_list(self, value):
        if self.problem_list.data:
            try:
                self.problem_list.data = json.loads(self.problem_list.data)
                if not isinstance(self.problem_list.data, list):
                    raise Exception()
            except Exception:
                raise ValidationError('Problem list must be list')
            for i in self.problem_list.data:
                if re.match('[a-z_]+-.+', i['problem']) is None:
                    raise ValidationError('Problem format error')
