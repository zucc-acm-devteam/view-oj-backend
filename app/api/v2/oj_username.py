from flask_login import current_user, login_required

from app.libs.error_code import Forbidden, Success
from app.libs.red_print import RedPrint
from app.models.oj_username import OJUsername
from app.validators.oj_username import CreateOJUsernameForm

api = RedPrint('oj_username')


@api.route("", methods=['POST'])
@login_required
def create_oj_username():
    # 创建 修改 删除
    form = CreateOJUsernameForm().validate_for_api().data_
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
    raise Success('OJ username has been created')
