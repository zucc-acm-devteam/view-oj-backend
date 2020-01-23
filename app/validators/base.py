from flask import request
from wtforms import Form, IntegerField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            raise ParameterException(msg=self.errors)
        return self

    @property
    def data_(self):
        data = dict()
        for key, value in self.__dict__.items():
            try:
                data[key] = value.data
            except AttributeError:
                pass
        return data


class SearchForm(BaseForm):
    page = IntegerField(validators=[DataRequired(message='Page cannot be empty')])
    page_size = IntegerField(validators=[DataRequired(message='Page size cannot be empty')])
    order = StringField()

    def validate_page(self, value):
        if self.page.data <= 0:
            raise ValidationError('Page must >= 1')

    def validate_page_size(self, value):
        if self.page_size.data > 100:
            raise ValidationError('Page size must <= 100')

    def validate_order(self, value):
        if self.order.data:
            if self.order.data != 'asc' and self.order.data != 'desc':
                raise ValidationError('Order must be `asc` or `desc`')
