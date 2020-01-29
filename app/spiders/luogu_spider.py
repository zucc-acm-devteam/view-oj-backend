import json
import re
import execjs
from urllib.parse import unquote

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.libs.spider_http import SpiderHttp


class LuoguHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.luogu.com.cn'
        }
        self.headers.update(headers)


class LuoguSpider(BaseSpider):
    @staticmethod
    def _get_user_id(username):
        url = 'https://www.luogu.com.cn/fe/api/user/search?keyword={}'.format(username)
        res = LuoguHttp().get(url=url)
        res_json = json.loads(res.text)
        res = None
        try:
            res = res_json['users'][0]['uid']
        except:
            pass
        return res

    @staticmethod
    def _change_problem_pid(problem_pid: str) -> (str, str):
        if problem_pid[0] == 'P':
            real_oj_name = 'luogu'
            problem_pid = problem_pid[1:]
        elif problem_pid[0] == 'C':
            real_oj_name = 'codeforces'
            problem_pid = problem_pid[2:]
        elif problem_pid[0] == 'S':
            real_oj_name = 'spoj'
            problem_pid = problem_pid[2:]
        elif problem_pid[0] == 'A':
            real_oj_name = 'atcoder'
            problem_pid = problem_pid[2:]
        elif problem_pid[0] == 'U':
            real_oj_name = 'uva'
            problem_pid = problem_pid[3:]
        else:
            raise Exception('problem can not resolve')
        return real_oj_name, problem_pid

    @classmethod
    def get_user_info(cls, oj_username, accept_problems):
        username = oj_username.oj_username
        uid = cls._get_user_id(username)
        if uid is None:
            return []
        url = 'https://www.luogu.com.cn/user/{}'.format(uid)
        res = LuoguHttp().get(url=url)
        res_raw = re.search(r'decodeURIComponent\("(.*)"\)\);', res.text).group(1)
        res_str = unquote(res_raw)
        res_json = json.loads(res_str)

        accept_problem_list = []
        for problem in res_json.get('currentData', dict()).get('passedProblems', dict()):
            real_oj, problem_pid = cls._change_problem_pid(problem['pid'])
            accept_problem_list.append({
                'oj': real_oj,
                'problem_pid': problem_pid,
                'accept_time': None
            })
        return accept_problem_list

    @classmethod
    def get_problem_info(cls, problem_id):
        url = 'https://www.luogu.com.cn/problem/P{}'.format(problem_id)
        res = LuoguHttp().get(url=url)

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
