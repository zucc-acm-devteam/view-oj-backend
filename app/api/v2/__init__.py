from flask import Blueprint

from app.api.v2 import (accept_problem, camp, meta, oj_username, problem_set,
                        session, task, user)


def create_blueprint_v2():
    bp_v2 = Blueprint('v2', __name__)

    user.api.register(bp_v2)
    session.api.register(bp_v2)
    oj_username.api.register(bp_v2)
    accept_problem.api.register(bp_v2)
    problem_set.api.register(bp_v2)
    task.api.register(bp_v2)
    camp.api.register(bp_v2)
    meta.api.register(bp_v2)
    return bp_v2
