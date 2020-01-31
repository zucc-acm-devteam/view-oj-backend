from flask import current_app

from app.models.accept_problem import AcceptProblem
from app.models.user import User


def task_calculate_user_rating(username=None):
    from task.task import task_f
    if username:
        user_list = [User.get_by_id(username)]
    else:
        user_list = User.search(status=1, page_size=1000)['data']
    for user in user_list:
        task_f.delay(calculate_user_rating, username=user.username)


def calculate_user_rating(username):
    rating = current_app.config['DEFAULT_USER_RATING']
    for i in AcceptProblem.search(username=username, order={'create_time': 'asc'}, page_size=10000)['data']:
        add_rating = calculate_user_add_rating(rating, i.problem.rating)
        i.modify(add_rating=add_rating)
        rating += add_rating


def calculate_user_add_rating(user_rating, problem_rating):
    return int((problem_rating / user_rating) ** 2 * 5)
