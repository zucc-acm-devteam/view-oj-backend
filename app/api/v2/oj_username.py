from flask_login import current_user, login_required

from app.libs.error_code import Forbidden, Success, DeleteSuccess
from app.libs.red_print import RedPrint
from app.models.oj_username import OJUsername
from app.validators.oj_username import CreateOJUsernameForm, ModifyOJUsernameForm, DeleteOJUsernameForm

api = RedPrint('oj_username')


@api.route("", methods=['POST'])
@login_required
def create_oj_username():
    form = CreateOJUsernameForm().validate_for_api().data_
    if current_user.permission != 1:
        if current_user.id != form['username']:
            raise Forbidden()
    if form['is_team_account'] and form['is_child_account']:
        raise Forbidden('Account can not be team while it\'s a child account')

    res = OJUsername.search(oj_id=form['oj_id'], username=form['username'])
    if res['meta']['count'] != 0:
        raise Forbidden('OJ username already exists')
    OJUsername.create(oj_id=form['oj_id'], username=form['username'], oj_username=form['oj_username'],
                      oj_password=form['oj_password'], is_team_account=form['is_team_account'],
                      is_child_account=form['is_child_account'])
    raise Success('OJ username has been created')


@api.route("/modify", methods=['POST'])
def modify_oj_username():
    form = ModifyOJUsernameForm().validate_for_api().data_
    if current_user.permission != 1:
        if current_user.id != form['username']:
            raise Forbidden()

    oj_username = OJUsername.get_by_id(form['oj_username_id'])
    if form['oj_username'] == oj_username.oj_username:
        oj_username.modify(oj_password=form['oj_password'])
    else:
        if not oj_username.is_team_account:
            oj_id = oj_username.oj_id
            username = oj_username.username
            oj_username.delete()
            OJUsername.create(oj_id=oj_id, username=username, oj_username=form['oj_username'],
                              oj_password=form['oj_password'])
        else:
            oj_username.modify(oj_username=form['oj_username'], oj_password=form['oj_password'])
    raise Success('OJ username has been modified')


@api.route("/delete", methods=['POST'])
def delete_oj_username():
    form = DeleteOJUsernameForm().validate_for_api().data_
    if current_user.permission != 1:
        if current_user.id != form['username']:
            raise Forbidden()
    res = OJUsername.search(oj_id=form['oj_id'], username=form['username'], oj_username=form['oj_username'])
    if res['meta']['count'] == 1:
        oj_username = res['data'][0]
        oj_username.delete()
        raise DeleteSuccess('OJ username has been deleted')
