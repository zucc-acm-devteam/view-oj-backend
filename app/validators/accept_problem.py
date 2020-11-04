from wtforms import StringField
from wtforms.validators import DataRequired

from app.validators.base import DateForm, SearchForm


class SearchAcceptProblemForm(SearchForm, DateForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])


class SearchAcceptProblemSummaryForm(DateForm):
    is_freshman = StringField()

    def validate_is_freshman(self, value):
        if self.is_freshman.data is None:
            self.is_freshman.data = False
        else:
            self.is_freshman.data = self.is_freshman.data.lower() == 'true'
