import json
import re
import time
from urllib.parse import unquote

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class LuoguHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.luogu.com.cn',
            'cookie': '__client_id=22325e412138d36d1b4c9f11654aacbb061c9c81; _uid=62916'
        }
        self.headers.update(headers)

    @staticmethod
    def _end_request(res, encoding):
        time.sleep(2)
        return res


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
        elif problem_pid[0] == 'T':
            real_oj_name = 'luogu-team'
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

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username

        page = 1
        finished = False
        success = False
        accept_problem_list = []
        while True:
            url = 'https://www.luogu.com.cn/record/list?user={}&page={}&status=12&_contentOnly=1'.format(username, page)
            res = LuoguHttp().get(url=url).json()
            for i in res['currentData']['records']['result']:
                success = True
                if i['status'] == 12:
                    real_oj, problem_pid = self._change_problem_pid(i['problem']['pid'])
                    accept_time = timestamp_to_str(i['submitTime'])
                    if accept_problems.get('{}-{}'.format(real_oj, problem_pid)) == accept_time:
                        finished = True
                        break
                    if real_oj != 'luogu-team':
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
