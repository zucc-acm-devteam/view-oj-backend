from flask import jsonify
from flask_login import login_required

from app import db
from app.libs.error_code import CreateSuccess
from app.libs.red_print import RedPrint
from app.libs.service import submit_calculate_user_rating_task
from app.libs.spider_service import (submit_crawl_accept_problem_task,
                                     submit_crawl_course_info_task,
                                     submit_crawl_problem_rating_task)
from app.validators.task import CreateTaskForm

api = RedPrint('task')


@api.route("", methods=['POST'])
@login_required
def create_task_api():
    form = CreateTaskForm().validate_for_api().data_
    if form['type'] == 'crawl_user_info':
        if form['kwargs']:
            submit_crawl_accept_problem_task(form['kwargs']['username'], form['kwargs']['oj_id'])
        else:
            submit_crawl_accept_problem_task()
    elif form['type'] == 'crawl_problem_info':
        submit_crawl_problem_rating_task(form['kwargs']['problem_id'])
    elif form['type'] == 'crawl_course_info':
        if form['kwargs']:
            submit_crawl_course_info_task(form['kwargs']['course_id'])
        else:
            submit_crawl_course_info_task()
    elif form['type'] == 'calculate_user_rating':
        if form['kwargs']:
            submit_calculate_user_rating_task(form['kwargs']['username'])
        else:
            submit_calculate_user_rating_task()
    return CreateSuccess('Task has been created')


@api.route("/summary", methods=['GET'])
def get_task_summary_api():
    res = db.session.execute("select count(*) from kombu_message where visible = 1 and queue_id = 1")
    res = res.fetchone()[0]
    task1 = res
    res = db.session.execute("select count(*) from kombu_message where visible = 1 and queue_id = 2")
    res = res.fetchone()[0]
    task2 = res
    db.session.execute("delete from kombu_message where visible = 0")
    db.session.commit()
    return jsonify({
        'code': 0,
        'data': {
            "redis1": task1,
            "redis2": task2,
        }
    })
