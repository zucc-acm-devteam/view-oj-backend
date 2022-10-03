import json
import re
import time
from urllib.parse import unquote

import requests

from app.config.secure import LUOGU_ID, LUOGU_PASSWORD
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.models.mapping import Mapping
from app.spiders.base_spider import BaseSpider


class LuoguHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'origin': 'https://www.luogu.com.cn'
        }
        self.headers.update(headers)

    @staticmethod
    def _end_request(res, encoding):
        time.sleep(2)
        return res


class LuoguSpider(BaseSpider):
    luogu_http = LuoguHttp()

    def __init__(self):
        try:
            self.check_cookie()
        except AssertionError:
            self.get_new_cookie()
            self.check_cookie()

    def check_cookie(self):
        self.luogu_http = LuoguHttp()
        mapping = Mapping.get_by_id('luogu-cookie')
        cookie = json.loads(mapping.value)
        for k, v in cookie.items():
            self.luogu_http.sess.cookies.set(k, v)
        assert self.check_login_status() is not None

    def get_new_cookie(self):
        self.luogu_http = LuoguHttp()
        self.login(LUOGU_ID, LUOGU_PASSWORD)
        assert self.check_login_status() is not None
        cookie = {}
        for i in self.luogu_http.sess.cookies:
            cookie[i.name] = i.value
        Mapping.get_by_id('luogu-cookie').modify(value=json.dumps(cookie, sort_keys=True))

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username

        page = 1
        finished = False
        success = False
        accept_problem_list = []
        while True:
            url = 'https://www.luogu.com.cn/record/list?user={}&page={}&status=12&_contentOnly=1'.format(username, page)
            res = self.luogu_http.get(url=url).json()
            for i in res['currentData']['records']['result']:
                success = True
                if i['status'] == 12:
                    try:
                        real_oj, problem_pid = self._change_problem_pid(i['problem']['pid'])
                    except Exception as e:
                        print(e)
                        continue
                    accept_time = timestamp_to_str(i['submitTime'])
                    if accept_problems.get('{}-{}'.format(real_oj, problem_pid)) == accept_time:
                        finished = True
                        continue
                    if not problem_pid.startswith('user-'):
                        accept_problem_list.append({
                            'oj': real_oj,
                            'problem_pid': problem_pid,
                            'accept_time': accept_time
                        })
            if finished:
                break
            if len(res['currentData']['records']['result']) != 20:
                break
            page += 1

        return {'success': success, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        url = 'https://www.luogu.com.cn/problem/P{}'.format(problem_id)
        res = self.luogu_http.get(url=url)

        try:
            res_raw = re.search(r'decodeURIComponent\("(.*)"\)\);', res.text).group(1)
            res_str = unquote(res_raw)
            res_json = json.loads(res_str)

            total = res_json['currentData']['problem']['totalSubmit']
            accept = res_json['currentData']['problem']['totalAccepted']

            rating = DEFAULT_PROBLEM_RATING

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    def _get_user_id(self, username):
        url = 'https://www.luogu.com.cn/fe/api/user/search?keyword={}'.format(username)
        res = self.luogu_http.get(url=url).json()
        try:
            return res['users'][0]['uid']
        except:
            return None

    @staticmethod
    def _change_problem_pid(problem_pid: str) -> (str, str):
        if problem_pid[0] == 'P':
            real_oj_name = 'luogu'
            problem_pid = problem_pid[1:]
        elif problem_pid[0] == 'T':
            real_oj_name = 'luogu'
            problem_pid = 'team-' + problem_pid[1:]
        elif problem_pid[0] == 'C':
            real_oj_name = 'codeforces'
            problem_pid = problem_pid[2:]
        elif problem_pid[0] == 'S':
            real_oj_name = 'spoj'
            problem_pid = problem_pid[2:]
        elif problem_pid[0] == 'A':
            real_oj_name = 'atcoder'
            problem_pid = problem_pid[2:]
        elif problem_pid.startswith("UVA"):
            real_oj_name = 'uva'
            problem_pid = problem_pid[3:]
        elif problem_pid[0] == 'U':
            real_oj_name = 'luogu'
            problem_pid = 'user-' + problem_pid[1:]
        else:
            raise Exception(f'problem {problem_pid} can not resolve')
        return real_oj_name, problem_pid

    def check_login_status(self):
        url = 'https://www.luogu.com.cn/'
        res = self.luogu_http.get(url=url)
        res_raw = re.search(r'decodeURIComponent\("(.*)"\)\);', res.text).group(1)
        res_str = unquote(res_raw)
        res_json = json.loads(res_str)
        return res_json['currentUser']['uid'] if res_json['currentUser'] else None

    def login(self, username, password):
        csrf_token = self._get_csrf_value()
        captcha = self._get_captcha()

        self.luogu_http.headers.update({
            'referer': 'https://www.luogu.com.cn/auth/login',
            'x-csrf-token': csrf_token,
            'content-type': 'application/json;charset=UTF-8'
        })
        url = 'https://www.luogu.com.cn/api/auth/userPassLogin'
        data = {
            'username': username,
            'password': password,
            'captcha': captcha
        }
        res = self.luogu_http.post(url=url, data=json.dumps(data)).json()
        if res.get('status'):
            print(res['errorMessage'])
            if '验证码' in res['errorMessage']:
                return self.login(username, password)
            raise Exception(res['errorMessage'])
        print(res)

        url = 'https://www.luogu.org/api/auth/syncLogin'
        data = {
            'syncToken': res['syncToken']
        }
        res = self.luogu_http.post(url=url, data=json.dumps(data)).json()
        print(res)

    def _get_captcha(self):
        self.luogu_http.headers.update({
            'referer': 'https://www.luogu.com.cn/auth/login',
            'content-type': None
        })
        url = 'https://www.luogu.com.cn/api/verify/captcha'
        res = self.luogu_http.get(url=url)
        import ddddocr
        ocr = ddddocr.DdddOcr(show_ad=False)
        captcha = ocr.classification(res.content)
        print(captcha)
        return captcha

    def _get_csrf_value(self):
        self.luogu_http.headers.update({
            'referer': 'https://www.luogu.com.cn/',
            'content-type': None
        })
        url = 'https://www.luogu.com.cn/auth/login'
        res = self.luogu_http.get(url=url)
        return re.search(r'<meta name="csrf-token" content="(.*?)">', res.text).group(1)


if __name__ == '__main__':
    from flask_app import app

    app.app_context().push()
    from app.models.oj_username import OJUsername

    oju = OJUsername()
    oju.oj_username = '417724'
    res = LuoguSpider().get_user_info(oju, {})
    print(res)
