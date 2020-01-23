from flask import jsonify
from flask_login import current_user, login_required

from app import redis
from app.libs.error_code import Forbidden, Success
from app.libs.red_print import RedPrint
from app.validators.forms import (NoAuthUsernameForm, OJIdForm,
                                  RefreshAcceptProblemForm,
                                  RefreshProblemRatingForm)
from tasks import (task_calculate_user_rating, task_crawl_accept_problem,
                   task_crawl_all_accept_problem, task_crawl_problem_rating,
                   task_refresh_oj_problem_rating)

api = RedPrint('task')


@api.route("/get_task_count", methods=['POST'])
def get_task_count_api():
    res = redis.llen('celery')
    return jsonify({
        'code': 0,
        'data': res
    })


@api.route("/refresh_all_data", methods=['POST'])
@login_required
def refresh_all_data_api():
    if not current_user.permission:
        raise Forbidden('Only administrators can operate')
    task_crawl_all_accept_problem.delay()
    return Success('Submit all refresh request successfully')


@api.route("/refresh_accept_problem", methods=['POST'])
@login_required
def refresh_accept_problem_api():
    form = RefreshAcceptProblemForm().validate_for_api()
    task_crawl_accept_problem.delay(form.username.data, form.oj_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_problem_rating", methods=['POST'])
@login_required
def refresh_problem_rating_api():
    form = RefreshProblemRatingForm().validate_for_api()
    task_crawl_problem_rating.delay(form.problem_id.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_user_rating", methods=['POST'])
def refresh_user_rating_api():
    form = NoAuthUsernameForm().validate_for_api()
    task_calculate_user_rating.delay(form.username.data)
    return Success('Submit refresh request successfully')


@api.route("/refresh_oj_problem_rating", methods=['POST'])
@login_required
def refresh_oj_problem_rating_api():
    form = OJIdForm().validate_for_api()
    task_refresh_oj_problem_rating.delay(form.oj_id.data)
    return Success('Submit refresh request successfully')
