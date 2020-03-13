import datetime
import json
import time

import requests

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.cookie import Cookie
from app.libs.helper import datetime_to_str, str_to_datetime
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class PintiaHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'application/json;charset=UTF-8'
        }
        self.headers.update(headers)

    @staticmethod
    def _end_request(res, encoding):
        time.sleep(2)
        return res


class PintiaSpider(BaseSpider):
    problem_set = [
        ('91827364500', 'Z'),  # ZOJ
        ('994805046380707840', 'L'),  # 天梯赛
        ('994805148990160896', 'T'),  # 顶级
        ('994805342720868352', 'A'),  # 甲级
        ('994805260223102976', 'B'),  # 乙级
    ]
    pintia_http = PintiaHttp()

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        password = oj_username.oj_password
        try:
            cookie = json.loads(oj_username.oj_cookies)
            headers = {
                'Cookie': Cookie.dict_to_str(cookie)
            }
            self.pintia_http.headers.update(headers)
            assert self.check_login_status() == username
        except:
            try:
                cookie = self._get_cookies(username, password)
            except:
                return {'success': False, 'data': []}
            headers = {
                'Cookie': Cookie.dict_to_str(cookie)
            }
            self.pintia_http.headers.update(headers)
            assert self.check_login_status() == username

        oj_username.modify(oj_cookies=json.dumps(cookie, sort_keys=True))

        self.check_in()

        accept_problem_list = []

        for problem_set_id, tag in self.problem_set:
            url = 'https://pintia.cn/api/problem-sets/{}/exams'.format(problem_set_id)
            res = self.pintia_http.get(url=url).json()
            try:
                exam_id = res['exam']['id']
            except:
                continue
            url = 'https://pintia.cn/api/valid-submissions?exam_id={}'.format(exam_id)
            res = self.pintia_http.get(url=url).json()
            try:
                submissions = res['submissions']
            except:
                return {'success': False, 'data': []}
            for submission in submissions:
                if submission['status'] != 'ACCEPTED':
                    continue
                accept_time = submission['submitAt'].replace('T', ' ').replace('Z', '')
                accept_time = datetime_to_str(str_to_datetime(accept_time) + datetime.timedelta(hours=8))
                pid = submission['problemSetProblem']['label']
                if tag == 'Z':
                    problem_id = pid
                    if accept_problems.get('zoj-' + problem_id) == accept_time:
                        continue
                    accept_problem_list.append({
                        'oj': 'zoj',
                        'problem_pid': problem_id,
                        'accept_time': accept_time
                    })
                else:
                    problem_id = '{}-{}'.format(tag, pid)
                    if accept_problems.get('pintia-' + problem_id) == accept_time:
                        continue
                    accept_problem_list.append({
                        'oj': 'pintia',
                        'problem_pid': problem_id,
                        'accept_time': accept_time
                    })

        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}

    def check_login_status(self):
        url = 'https://pintia.cn/api/u/current'
        res = self.pintia_http.get(url=url).json()
        if not res.get('user'):
            return None
        return res['user']['email']

    @staticmethod
    def _get_cookies(email, password):
        url = 'http://121.40.130.181:5000/api/get-pta-cookies'
        res = requests.post(url=url, timeout=300, data={
            'username': email,
            'password': password
        }).json()
        if res.get('status') != 'ok':
            raise Exception(res.get('error'))
        return Cookie.str_to_dict(res['result'])

    def check_in(self):
        url = 'https://pintia.cn/api/users/checkin'
        res = self.pintia_http.post(url=url).json()
        print(res)
