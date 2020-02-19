import json

from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.models.oj import OJ
from app.models.problem import Problem
from app.models.user import User
from app.validators.base import BaseForm


class CreateTaskForm(BaseForm):
    type = StringField(validators=[DataRequired(message='Task type cannot be empty')])
    kwargs = StringField()

    def validate_type(self, value):
        if self.kwargs.data is not None:
            try:
                self.kwargs.data = json.loads(self.kwargs.data)
                if not isinstance(self.kwargs.data, dict):
                    raise Exception()
            except Exception:
                raise ValidationError('kwargs format error')

        if self.type.data == 'crawl_user_info':
            if self.kwargs.data is not None:
                if self.kwargs.data.get('username') is None or self.kwargs.data.get('oj_id') is None:
                    raise ValidationError('kwargs missing parameters')
                if User.get_by_id(self.kwargs.data['username']) is None:
                    raise ValidationError('User does not exist')
                if OJ.get_by_id(self.kwargs.data['oj_id']) is None:
                    raise ValidationError('OJ does not exist')
        elif self.type.data == 'crawl_problem_info':
            if self.kwargs.data is None or self.kwargs.data.get('problem_id') is None:
                raise ValidationError('kwargs missing parameters')
            if Problem.get_by_id(self.kwargs.data['problem_id']) is None:
                raise ValidationError('Problem does not exist')
        elif self.type.data == 'calculate_user_rating':
            if self.kwargs.data is not None:
                if self.kwargs.data.get('username') is None:
                    raise ValidationError('kwargs missing parameters')
                if User.get_by_id(self.kwargs.data['username']) is None:
                    raise ValidationError('User does not exist')
        else:
            raise ValidationError('Unknown task type')
