import json
import re

from bs4 import BeautifulSoup

from app.config.secure import ZUCC_ID, ZUCC_PASSWORD
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.cookie import Cookie
from app.libs.spider_http import SpiderHttp
from app.models.mapping import Mapping
from app.spiders.base_spider import BaseSpider


class ZuccSpider(BaseSpider):
    zucc_http = SpiderHttp()

    def __init__(self):
        mapping = Mapping.get_by_id('zucc-cookie')
        try:
            cookie = json.loads(mapping.value)
            headers = {
                'Cookie': Cookie.dict_to_str(cookie)
            }
            self.zucc_http.headers.update(headers)
            assert self.check_login_status() == ZUCC_ID
        except:
            self.zucc_http.headers.update({'Cookie': None})
            self.login(ZUCC_ID, ZUCC_PASSWORD)
            assert self.check_login_status() == ZUCC_ID

            cookie = {}
            for i in self.zucc_http.sess.cookies:
                cookie[i.name] = i.value

            mapping.modify(value=json.dumps(cookie, sort_keys=True))

    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        if not self._judge_user(username):
            return {'success': False, 'data': []}
        accept_problem_list = []
        url = 'http://acm.zucc.edu.cn/status.php?user_id={}'.format(username)
        ok = False
        while not ok:
            res = self.zucc_http.get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            trs = soup.find('tbody').find_all('tr')
            next = -1
            if not trs:
                break
            for tr in trs:
                tds = tr.find_all('td')
                next = int(tds[0].text)
                status = tds[3].find_all('a')[0]['class']
                if 'label-success' not in status:
                    continue
                problem_id = tds[2].text
                accept_time = tds[8].text
                accept_time = re.findall(r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}', accept_time)[0]
                if accept_problems.get('zucc-' + problem_id) == accept_time:
                    ok = True
                    break
                accept_problem_list.append({
                    'oj': 'zucc',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
            new_url = 'http://acm.zucc.edu.cn/status.php?user_id={}&top={}'.format(username, next - 1)
            if new_url == url:
                break
            url = new_url
        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        url = 'http://acm.zucc.edu.cn/problem.php?id={}'.format(problem_id)
        res = self.zucc_http.get(url=url)
        try:
            total = int(re.search(r'Submit: </span>(\d+)(&nbsp;)*<span', res.text).group(1))
            accept = int(re.search(r'Solved: </span>(\d+)(&nbsp;)*<br>', res.text).group(1))
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    def _judge_user(self, username):
        url = 'http://acm.zucc.edu.cn/userinfo.php?user={}'.format(username)
        res = self.zucc_http.get(url=url)
        return not re.findall(r"No such User!", res.text)

    def check_login_status(self):
        url = 'http://acm.zucc.edu.cn/template/bs3/profile.php'
        res = self.zucc_http.get(url=url)
        try:
            return re.search(r'document\.getElementById\("profile"\)\.innerHTML="(.*)";', res.text).group(1)
        except:
            return None

    def _get_csrf_value(self):
        url = 'http://acm.zucc.edu.cn/csrf.php'
        res = self.zucc_http.get(url=url)
        return re.search(r'value="(.*?)"', res.text).group(1)

    def login(self, username, password):
        url = 'http://acm.zucc.edu.cn/login.php'
        data = {
            'user_id': username,
            'password': password,
            'csrf': self._get_csrf_value()
        }
        res = self.zucc_http.post(url=url, data=data)


if __name__ == '__main__':
    from app import create_app
    from app.models.oj_username import OJUsername
    oj_username = OJUsername()
    oj_username.oj_username = '31801054'
    create_app().app_context().push()

    res = ZuccSpider().get_user_info(oj_username, {})
    print(res)
