from flask import jsonify
from flask_login import login_required

from app import redis1, redis2
from app.libs.error_code import CreateSuccess
from app.libs.red_print import RedPrint
from app.libs.service import task_calculate_user_rating
from app.libs.spider_service import task_crawl_accept_problem, task_crawl_problem_rating
from app.validators.task import CreateTaskForm

api = RedPrint('task')


@api.route("", methods=['POST'])
@login_required
def create_task_api():
    form = CreateTaskForm().validate_for_api().data_
    if form['type'] == 'craw_user_info':
        if form['kwargs']:
            task_crawl_accept_problem(form['kwargs']['username'], form['kwargs']['oj_id'])
        else:
            task_crawl_accept_problem()
    elif form['type'] == 'craw_problem_info':
        task_crawl_problem_rating(form['kwargs']['problem_id'])
    elif form['calculate_user_rating']:
        if form['kwargs']:
            task_calculate_user_rating(form['kwargs']['username'])
        else:
            task_calculate_user_rating()
    return CreateSuccess('Task has been created')


@api.route("/summary", methods=['GET'])
def get_task_summary_api():
    return jsonify({
        'code': 0,
        'data': {
            "redis1": redis1.llen('celery'),
            "redis2": redis2.llen('celery')
        }
    })
