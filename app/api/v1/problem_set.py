from flask import jsonify
from flask_login import login_required

from app.libs.error_code import Success
from app.libs.red_print import RedPrint
from app.models.accept_problem import get_accept_problem_by_problem_list
from app.models.problem_set import (create_problem_set, delete_problem_set,
                                    get_problem_set_by_problem_id,
                                    get_problem_set_list, modify_problem_set)
from app.models.user import get_user_list
from app.validators.forms import (ModifyProblemSetForm, ProblemSetIdForm,
                                  ProblemSetInfoForm)

api = RedPrint('problem_set')


@api.route("/create_problem_set", methods=['POST'])
@login_required
def create_problem_set_api():
    form = ProblemSetInfoForm().validate_for_api()
    create_problem_set(form.problem_set_name.data, form.problem_id_list.data)
    return Success('Create problem set successful')


@api.route("/modify_problem_set", methods=['POST'])
@login_required
def modify_problem_set_api():
    form = ModifyProblemSetForm().validate_for_api()
    modify_problem_set(form.problem_set_id.data, form.problem_set_name.data)
    return Success('Modify problem set successful')


@api.route("/delete_problem_set", methods=['POST'])
@login_required
def delete_problem_set_api():
    form = ProblemSetIdForm().validate_for_api()
    delete_problem_set(form.problem_set_id.data)
    return Success('Delete problem set successful')


@api.route("/get_problem_set_list", methods=['POST'])
def get_problem_set_list_api():
    res = get_problem_set_list()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_problem_set_detail", methods=['POST'])
def get_problem_set_detail_api():
    form = ProblemSetIdForm().validate_for_api()
    user_list = get_user_list()
    problem_list = [{
        'problem_id': i.problem_id,
        'oj_id': i.problem.oj_id,
        'oj_name': i.problem.oj.name,
        'problem_pid': i.problem.problem_pid,
        'problem_url': i.problem.url
    } for i in get_problem_set_by_problem_id(form.problem_set_id.data).problem]
    res = list()
    for user in user_list:
        if user['status']:
            res.append({
                'username': user['username'],
                'nickname': user['nickname'],
                'data': [{
                    'problem_id': i.problem_id,
                    'create_time': i.create_time
                } for i in
                    get_accept_problem_by_problem_list(user['username'], [i['problem_id'] for i in problem_list])]
            })
    return jsonify({
        'code': 0,
        'data': {
            'problem_list': problem_list,
            'data': res
        }
    })
