import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import datetime_to_str, str_to_datetime
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class LojSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        try:
            self._get_user_id(username)
        except:
            return {'success': False, 'data': []}
        success = True
        accept_problem_list = []
        url = 'https://loj.ac/submissions?submitter={}&status=Accepted'.format(username)
        ok = False
        bottom = -1
        while True:
            res = SpiderHttp().get(url=url)
            itemlist = re.findall(r'const itemList = ([\s\S]+?);', res.text)[0]
            datalist = json.loads(itemlist)
            if not datalist:
                break
            for data in datalist:
                data = data['info']
                problem_id = str(data['problemId'])
                accept_time = self._make_time_strict(data['submitTime'])
                bottom = data['submissionId']
                if accept_problems.get('loj-' + problem_id) == accept_time:
                    ok = True
                    break
                accept_problem_list.append({
                    'oj': 'loj',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
            if ok:
                break
            url = 'https://loj.ac/submissions?submitter={}' \
                  '&status=Accepted&currPageBottom={}&page=1'.format(username, bottom)

        return {'success': success, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        try:
            url = 'http://loj.ac/problems/search?keyword={}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'<td>(\d+)</td>\n.*<td>(\d+)</td>', res.text)[0]
            accept = int(data[0])
            total = int(data[1])
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_user_id(username):
        url = 'http://loj.ac/find_user?nickname={}'.format(username)
        res = SpiderHttp().get(url=url)
        uid = re.findall(r'user/(\d+)', res.url)[0]
        return uid

    @staticmethod
    def _make_time_strict(time):
        return datetime_to_str(str_to_datetime(time))
