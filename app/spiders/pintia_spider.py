import json
import time
import requests

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.libs.cookie import Cookie
from app.libs.spider_http import SpiderHttp


class PintiaHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'Accept': 'application/json;charset=UTF-8'
        }
        self.headers.update(headers)

    limit: int = 500
    lastreq: int = 0

    def time(self):
        return int(time.time() * 1000)

    def checklimit(self):
        return self.time() - self.lastreq >= self.limit

    def get(self, **kwargs):
        while not self.checklimit():
            time.sleep(self.limit / 1000)
        self.lastreq = self.time()
        return self._request('GET', **kwargs)

    def post(self, **kwargs):
        while not self.checklimit():
            time.sleep(self.limit / 1000)
        self.lastreq = self.time()
        return self._request('POST', **kwargs)


class PintiaSpider(BaseSpider):
    problem_set = [
        ('91827364500', 'Z'),  # ZOJ
        ('994805046380707840', 'L'),  # 天梯赛
        ('994805148990160896', 'T'),  # 顶级
        ('994805342720868352', 'A'),  # 甲级
        ('994805260223102976', 'B'),  # 乙级
    ]
    pintia_http = PintiaHttp()

    @classmethod
    def get_user_info(cls, oj_username, accept_problems):
        username = oj_username.oj_username
        password = oj_username.oj_password
        try:
            cookies = json.loads(oj_username.oj_cookies)
            headers = {
                'Cookie': Cookie.dict_to_str(cookies)
            }
            cls.pintia_http.headers.update(headers)
            assert cls.check_cookies(username)
        except:
            try:
                cookies = PintiaSpider._get_cookies(username, password)
            except:
                return {'success': False, 'data': []}
            oj_username.modify(oj_cookies=json.dumps(cookies))
            headers = {
                'Cookie': Cookie.dict_to_str(cookies)
            }
            cls.pintia_http.headers.update(headers)
        accept_problem_list = []

        for problem_set_id, tag in cls.problem_set:
            url = 'https://pintia.cn/api/problem-sets/{}/exams'.format(problem_set_id)
            res = cls.pintia_http.get(url=url).json()
            try:
                exam_id = res['exam']['id']
            except:
                continue
            url = 'https://pintia.cn/api/valid-submissions?exam_id={}'.format(exam_id)
            res = cls.pintia_http.get(url=url).json()
            try:
                submissions = res['submissions']
            except:
                return {'success': False, 'data': []}
            for submission in submissions:
                if submission['status'] != 'ACCEPTED':
                    continue
                accept_time = submission['submitAt'].replace('T', ' ').replace('Z', '')
                problem_id = '{}-{}'.format(tag, submission['problemSetProblem']['label'])
                if accept_time == accept_problems.get(problem_id):
                    continue
                accept_problem_list.append({
                    'oj': 'pintia',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })

        return {'success': True, 'data': accept_problem_list}

    @classmethod
    def get_problem_info(cls, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}

    @classmethod
    def check_cookies(cls, email):
        url = 'https://pintia.cn/api/u/current'
        res = cls.pintia_http.get(url=url).json()
        if not res.get('user'):
            return False
        if res['user']['email'] != email:
            return False
        return True

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
