from flask import jsonify

from app.libs.red_print import RedPrint
from app.models.accept_problem import AcceptProblem
from app.validators.accept_problem import SearchAcceptProblemForm

api = RedPrint('accept_problem')


@api.route("", methods=['GET'])
def search_accept_problem_api():
    form = SearchAcceptProblemForm().validate_for_api().data_
    res = AcceptProblem.search(**form)
    return jsonify({
        'code': 0,
        'data': res
    })
