from wtforms import StringField

from app.validators.base import SearchForm, DateForm


class SearchAcceptProblemForm(SearchForm, DateForm):
    username = StringField()
