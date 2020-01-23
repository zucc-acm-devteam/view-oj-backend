from flask import jsonify
from flask_login import login_required
from sqlalchemy.sql.functions import current_user

from app.libs.error_code import Success, Forbidden
from app.libs.red_print import RedPrint
from app.models.oj_username import OJUsername
from app.validators.oj_username import OJUsernameForm, SearchOJUsernameForm

api = RedPrint('oj_username')


@api.route("", metheds=['POST'])
@login_required
def create_oj_username():
    # 创建 修改 删除
    form = OJUsernameForm().validate_for_api().data_
    if current_user.permission != -1:
        if current_user.id != form['username']:
            raise Forbidden()

    res = OJUsername.search(oj_id=form['oj_id'], username=form['username'])
    if res['meta']['count'] == 1:
        oj_username = res['data'][0]
        if form['oj_username']:
            oj_username.modify(oj_username=form['oj_username'])
        else:
            oj_username.delete()
    else:
        OJUsername.create(oj_id=form['oj_id'], username=form['username'], oj_username=form['oj_username'])
    return Success('OJ username has been created')


@api.route("", metheds=['GET'])
def search_oj_username():
    form = SearchOJUsernameForm().validate_for_api().data_
    res = OJUsername.search(**form)
    return jsonify({
        'code': 0,
        'data': res
    })
