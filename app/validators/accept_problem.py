from wtforms import StringField

from app.validators.base import DateForm, SearchForm


class SearchAcceptProblemForm(SearchForm, DateForm):
    username = StringField()
