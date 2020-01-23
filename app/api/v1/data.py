from flask import jsonify

from app.libs.red_print import RedPrint
from app.models.accept_problem import (get_accept_problem_count_by_date,
                                       get_accept_problem_date_distributed,
                                       get_accept_problem_list_by_date,
                                       get_accept_problem_oj_distributed,
                                       get_rating_rank_list, get_rating_trend)
from app.models.oj import get_oj_list
from app.models.problem import get_problem_by_problem_info
from app.models.user import get_user_list
from app.validators.forms import (DateForm, InquireCountForm, InquireForm,
                                  InquireProblemIdForm, NoAuthUsernameForm)

api = RedPrint('data')


@api.route("/get_all_accept_problem_count", methods=['POST'])
def get_all_accept_problem_count_api():
    form = DateForm().validate_for_api()
    res = list()
    for user in get_user_list():
        if user['status']:
            res.append({
                'username': user['username'],
                'nickname': user['nickname'],
                'group': user['group'],
                'accept_problem_count': get_accept_problem_count_by_date(user['username'], form.start_date.data,
                                                                         form.end_date.data)
            })
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_rating_rank_list", methods=['POST'])
def get_rating_rank_list_api():
    res = get_rating_rank_list()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_accept_problem", methods=['POST'])
def get_accept_problem_api():
    form = InquireForm().validate_for_api()
    res = get_accept_problem_list_by_date(form.username.data, form.start_date.data, form.end_date.data,
                                          form.page.data, form.page_size.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_accept_problem_oj_distributed", methods=['POST'])
def get_accept_problem_distributed_api():
    form = NoAuthUsernameForm().validate_for_api()
    res = get_accept_problem_oj_distributed(form.username.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_accept_problem_count_distributed", methods=['POST'])
def get_accept_problem_count_distributed_api():
    form = InquireCountForm().validate_for_api()
    res = get_accept_problem_date_distributed(form.username.data, form.start_date.data, form.end_date.data)
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_problem_id", methods=['POST'])
def get_problem_id_api():
    form = InquireProblemIdForm().validate_for_api()
    res = get_problem_by_problem_info(form.oj_id.data, form.problem_pid.data)
    if res:
        res = res.id
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_oj_list", methods=['POST'])
def get_oj_list_api():
    res = get_oj_list()
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/get_rating_trend", methods=['POST'])
def get_rating_trend_api():
    form = NoAuthUsernameForm().validate_for_api()
    res = get_rating_trend(form.username.data)
    return jsonify({
        'code': 0,
        'data': res
    })
