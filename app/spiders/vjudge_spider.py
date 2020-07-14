from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class VjudgeSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        accept_problem_list = []
        success = False
        url = "https://vjudge.net/status/data/"
        start = 0
        length = 20
        ok = False
        while not ok:
            data = {
                'un': username,
                'start': start,
                'length': length
            }
            res = SpiderHttp().post(url=url, data=data).json()
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
