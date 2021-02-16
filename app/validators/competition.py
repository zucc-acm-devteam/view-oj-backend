from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from app.validators.base import DateTimeForm, BaseForm
from wtforms.validators import ValidationError


class BaseSearchCompetitionForm(BaseForm):
    page = IntegerField()
    page_size = IntegerField()

    def validate_page(self, value):
        if self.page.data:
            self.page.data = int(self.page.data)
            if self.page.data <= 0:
                raise ValidationError('Page must >= 1')

    def validate_page_size(self, value):
        if self.page_size.data:
            self.page_size.data = int(self.page_size.data)
            if self.page_size.data > 100:
                raise ValidationError('Page size must <= 100')


class CreateCompetitionForm(DateTimeForm):
    name = StringField(validators=[DataRequired(message='competition name cannot be empty')])
    link = StringField(validators=[DataRequired(message='competition link cannot be empty')])
    remark = StringField()


class ModifyCompetitionForm(DateTimeForm):
    name = StringField()
    link = StringField()
    remark = StringField()
