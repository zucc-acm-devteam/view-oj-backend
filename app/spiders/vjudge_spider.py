import json

from app.libs.cookie import Cookie
from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class VjudgeSpider(BaseSpider):
    vjudge_http = SpiderHttp()

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        password = oj_username.oj_password
        try:
            cookie = json.loads(oj_username.oj_cookies)
            headers = {
                'Cookie': Cookie.dict_to_str(cookie)
            }
            self.vjudge_http.headers.update(headers)
            assert self.check_login_status() == username
        except:
            try:
                cookie = self._get_cookies(username, password)
            except:
                return {'success': False, 'data': []}
            headers = {
                'Cookie': Cookie.dict_to_str(cookie)
            }
            self.vjudge_http.headers.update(headers)
            assert self.check_login_status() == username

        oj_username.modify(oj_cookies=json.dumps(cookie, sort_keys=True))

        accept_problem_list = []
        success = False
        start = 0
        length = 20
        ok = False
        while not ok:
            url = "https://vjudge.net/status/data/?&length=20&res=1&start={}&un={}".format(start, username)
            res = self.vjudge_http.get(url=url).json()
            if not res['data']:
                break
            success = True
            for submission in res['data']:
                if submission['statusCanonical'] != 'AC':
                    continue
                time_stamp = submission['time'] / 1000
                accept_time = timestamp_to_str(time_stamp)
                oj = self._change_oj_name(submission['oj'])
                problem_id = submission['probNum']
                if accept_problems.get('{}-{}'.format(oj, problem_id)) == accept_time:
                    ok = True
                    continue
                accept_problem_list.append({
                    'oj': oj,
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
            start += length

        return {'success': success, 'data': accept_problem_list}

    def check_login_status(self):
        url = 'https://vjudge.net/user/update'
        res = self.vjudge_http.get(url=url).json()
        return res.get('username', None)

    def _get_cookies(self, username, password):
        url = 'https://vjudge.net/user/login'
        data = {
            'username': username,
            'password': password
        }
        res = self.vjudge_http.post(url=url, data=data).text
        if res == 'success':
            return Cookie.str_to_dict(Cookie.dict_to_str(self.vjudge_http.sess.cookies))
        raise Exception(res)

    def get_problem_info(self, problem_id):
        pass

    @staticmethod
    def _change_oj_name(name):
        name = name.lower()
        if name == 'gym':
            name = 'codeforces'
        elif name == 'zju':
            name = 'zoj'
        elif name == 'pku':
            name = 'poj'
        elif name == '计蒜客':
            name = 'jisuanke'
        elif name == 'uvalive':
            name = 'uva'
        elif name == 'libreoj':
            name = 'loj'
        return name
