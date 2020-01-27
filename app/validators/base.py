import datetime
import json

from flask import request
from wtforms import DateField, Form, IntegerField, StringField
from wtforms.validators import ValidationError

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
    page = IntegerField()
    page_size = IntegerField()
    order = StringField()

    def validate_page(self, value):
        if self.page.data:
            if self.page.data <= 0:
                raise ValidationError('Page must >= 1')

    def validate_page_size(self, value):
        if self.page_size.data:
            if self.page_size.data > 100:
                raise ValidationError('Page size must <= 100')

    def validate_order(self, value):
        if self.order.data:
            try:
                self.order.data = json.loads(self.order.data)
            except Exception:
                raise ValidationError('Order must be dict')
            for i in self.order.data.values():
                if i not in ['asc', 'desc']:
                    raise ValidationError('Order value must be `asc` or `desc`')


class DateForm(Form):
    start_date = DateField()
    end_date = DateField()

    def validate_start_date(self, value):
        if self.start_date.data:
            self.start_date.data = datetime.datetime.strptime(self.start_date.data, '%Y-%m-%d').date()
        else:
            self.start_date.data = datetime.date.today() - datetime.timedelta(days=6)

    def validate_end_date(self, value):
        if self.end_date.data:
            self.end_date.data = datetime.datetime.strptime(self.end_date.data, '%Y-%m-%d').date()
        else:
            self.end_date.data = datetime.date.today()
