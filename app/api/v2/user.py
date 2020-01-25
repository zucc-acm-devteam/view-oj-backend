from flask import jsonify
from flask_login import current_user, login_required

from app.libs.auth import admin_only
from app.libs.error_code import CreateSuccess, Forbidden, NotFound, Success
from app.libs.red_print import RedPrint
from app.models.user import User
from app.validators.user import CreateUserForm, ModifyUserForm, SearchUserForm

api = RedPrint('user')


@api.route("/<string:id_>", methods=['GET'])
@login_required
def get_user_api(id_):
    if current_user.permission != -1:
        if current_user.id != id_:
            raise Forbidden()

    user = User.get_by_id(id_)
    if user is None:
        return NotFound('User not found')
    return jsonify({
        "code": 0,
        "data": user
    })


@api.route("", methods=['POST'])
@login_required
@admin_only
def create_user_api():
    form = CreateUserForm().validate_for_api().data_
    form['nickname'] = form['password'] = form['username']
    form['permission'] = 0
    form['status'] = 1
    User.create(**form)
    return CreateSuccess('User has been created')


@api.route("/<string:id_>", methods=['PATCH'])
@login_required
def modify_user_api(id_):
    form = ModifyUserForm().validate_for_api().data_
    if current_user.permission != -1:
        if current_user.id != id_:
            raise Forbidden()
        if form['group'] or form['permission'] or form['status']:
            raise Forbidden()

    user = User.get_by_id(id_)
    if user is None:
        return NotFound('User not found')

    user.modify(**form)
    return Success('User has been modified')


@api.route("", methods=['GET'])
@admin_only
def search_user_api():
    form = SearchUserForm().validate_for_api().data_
    res = User.search(**form)
    fields = User.fields.copy()
    fields.remove('rating')
    fields.remove('oj_username')
    for user in res['data']:
        user.fields = fields
    return jsonify({
        'code': 0,
        'data': res
    })
