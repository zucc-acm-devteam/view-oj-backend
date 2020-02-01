import json

from flask import current_app

from app.libs.cookie import Cookie
from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.models.mapping import Mapping
from app.spiders.base_spider import BaseSpider


class VjudgeHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        self.headers.update(headers)


class VjudgeSpider(BaseSpider):
    vjudge_http = VjudgeHttp()

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        accept_problem_list = []
        max_id = ''
        finished = False
        success = False
        while True:
            url = "https://vjudge.net/user/submissions?" \
                  "username={}&pageSize=500&status=ac&maxId={}".format(username, max_id)
            res = self.vjudge_http.get(url=url).json()
            if not res['data']:
                break
            for i in res['data']:
                success = True
                if i[4] == 'AC':
                    oj_name = self._change_oj_name(i[2])
                    problem_pid = i[3]
                    accept_time = timestamp_to_str(i[9] // 1000)
                    if accept_problems.get("{}-{}".format(oj_name, problem_pid)) == accept_time:
                        finished = True
                        break
                    accept_problem_list.append({
                        'oj': oj_name,
                        'problem_pid': problem_pid,
                        'accept_time': accept_time
                    })
                max_id = i[0] - 1
            if finished:
                break
        return {'success': success, 'data': accept_problem_list}

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
        return name

    @classmethod
    def login(cls, username, password):
        url = 'https://vjudge.net/user/login'
        cls.vjudge_http.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        data = {
            'username': username,
            'password': password
        }
        res = cls.vjudge_http.post(url=url, data=data)
        cls.vjudge_http.headers.pop('Content-Type')
        return res.text == 'success'

    @classmethod
    def check_cookie(cls):
        url = 'https://vjudge.net/user/checkLogInStatus'
        res = cls.vjudge_http.post(url=url)
        return res.text == 'true'
