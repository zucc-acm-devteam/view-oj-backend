from flask import jsonify
from flask_login import current_user, login_required, login_user, logout_user

from app.libs.error_code import AuthFailed, DeleteSuccess, Success
from app.libs.red_print import RedPrint
from app.models.user import User
from app.validators.session import LoginForm, SSOLoginForm

api = RedPrint('session')


@api.route("", methods=['GET'])
@login_required
def get_session_api():
    user = current_user
    user.fields = ['username', 'nickname', 'group', 'permission', 'status']
    return jsonify({
        'code': 0,
        'data': user
    })


@api.route("", methods=['POST'])
def create_session_api():
    form = LoginForm().validate_for_api().data_
    user = User.get_by_id(form['username'])
    if user is None:
        raise AuthFailed('User not found')
    if not user.check_password(form['password']):
        raise AuthFailed('Wrong username or password')
    login_user(user, remember=True)
    raise Success('Login successful')


@api.route("/ssoLogin", methods=['POST'])
def create_session_sso_api():
    form = SSOLoginForm().validate_for_api().data_
    username = form['username']
    ticket = form['ticket']
    import requests
    check_url = 'https://api.zuccacm.top/sso/v1/ticket/check'
    resp = requests.post(url=check_url, json={
        'username': username,
        'ticket': ticket
    })
    if resp.status_code != 200:
        raise AuthFailed('验证失败')
    user = User.get_by_id(form['username'])
    if user is None:
        import random
        from string import digits, ascii_letters
        password = ''.join(random.sample(ascii_letters + digits, 20))
        user = User.create(
            username=username, nickname=username,
            password=password, group='未分组'
        )
    login_user(user)
    raise Success('Login successful')


@api.route("", methods=['DELETE'])
def delete_session_api():
    logout_user()
    raise DeleteSuccess('Logout successful')
