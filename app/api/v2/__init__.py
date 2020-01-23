from flask import Blueprint

from app.api.v2 import session, user, oj_username


def create_blueprint_v2():
    bp_v2 = Blueprint('v2', __name__)

    user.api.register(bp_v2)
    session.api.register(bp_v2)
    oj_username.api.register(bp_v2)
    return bp_v2
