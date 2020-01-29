from flask import jsonify

from app.libs.red_print import RedPrint
from app.models.accept_problem import AcceptProblem
from app.validators.accept_problem import SearchAcceptProblemForm, SearchAcceptProblemSummaryForm

api = RedPrint('accept_problem')


@api.route("", methods=['GET'])
def search_accept_problem_api():
    form = SearchAcceptProblemForm().validate_for_api().data_
    res = AcceptProblem.search(**form)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/summary", methods=['GET'])
def search_accept_problem_summary_api():
    from app.models.user import User
    form = SearchAcceptProblemSummaryForm().validate_for_api().data_
    res = []
    for i in User.search(status=1, page_size=1000)['data']:
        res.append({
            'user': i,
            'num': AcceptProblem.search(username=i.username, **form, page_size=1)['meta']['count']
        })
    return jsonify({
        'code': 0,
        'data': res
    })
