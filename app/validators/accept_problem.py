from wtforms import StringField
from wtforms.validators import DataRequired

from app.validators.base import DateForm, SearchForm


class SearchAcceptProblemForm(SearchForm, DateForm):
    username = StringField(validators=[DataRequired(message='Username cannot be empty')])


class SearchAcceptProblemSummaryForm(DateForm):
    pass
