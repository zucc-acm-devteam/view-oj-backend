import json

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import datetime_to_str, str_to_datetime
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class LojSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        if not self._find_user_id(username):
            return {'success': False, 'data': []}
        accept_problem_list = []
        url = 'https://api.loj.ac.cn/api/submission/querySubmission'
        request_data = {
            'locale': 'zh_CN',
            'status': 'Accepted',
            'submitter': username,
            'takeCount': 10
        }
        has_smaller = True
        now = -1
        try:
            while has_smaller:
                if now != -1:
                    request_data['maxId'] = now - 1
                res = SpiderHttp().post(url=url, data=json.dumps(request_data), headers={
                    'Content-Type': 'application/json'
                }).json()
                has_smaller = res['hasSmallerId']
                for data in res['submissions']:
                    problem_id = str(data['problem']['id'])
                    accept_time = self._make_time_strict(data['submitTime'])
                    now = data['id']
                    if accept_problems.get('loj-' + problem_id) == accept_time:
                        break
                    accept_problem_list.append({
                        'oj': 'loj',
                        'problem_pid': problem_id,
                        'accept_time': accept_time
                    })
        except:
            return {'success': False, 'data': {}}

        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}

    @staticmethod
    def _find_user_id(username):
        url = 'https://api.loj.ac.cn/api/user/searchUser?query={}'.format(username)
        res = SpiderHttp().get(url=url)
        ok = False
        try:
            for i in res.json()['userMetas']:
                if i['username'] == username:
                    ok = True
                    break
        except:
            pass
        return ok

    @staticmethod
    def _make_time_strict(time):
        import datetime
        time = time.replace('T', ' ')[:-5]
        time = datetime_to_str(str_to_datetime(time) + datetime.timedelta(hours=8))
        return time
