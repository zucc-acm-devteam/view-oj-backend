import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class HysbzHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            'host': 'www.lydsy.com'
        }
        self.headers.update(headers)


class HysbzSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        if not self._judge_user(username):
            return {'success': False, 'data': []}
        accept_problem_list = []
        url = 'http://www.lydsy.com/JudgeOnline/status.php?user_id={}&jresult=4'.format(username)
        ok = False
        while not ok:
            res = HysbzHttp().get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            trs = soup.find_all('table')[-1].find_all('tr')[1:]
            next = -1
            if not trs:
                break
            for tr in trs:
                tds = tr.find_all('td')
                problem_id = tds[2].text
                accept_time = tds[8].text
                if accept_problems.get('hysbz-' + problem_id) == accept_time:
                    ok = True
                    continue
                accept_problem_list.append({
                    'oj': 'hysbz',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
                next = int(tds[0].text)
            url = 'http://www.lydsy.com/JudgeOnline/status.php?user_id={}&jresult=4&top={}'.format(username,
                                                                                         next - 1)
        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        url = 'https://www.lydsy.com/JudgeOnline/problem.php?id={}'.format(problem_id)
        res = HysbzHttp().get(url=url)

        try:
            total = int(re.search(r'<span class=green>Submit: </span>(\d+)&nbsp;&nbsp;', res.text).group(1))
            accept = int(re.search(r'<span class=green>Solved: </span>(\d+)<br>', res.text).group(1))
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    @staticmethod
    def _judge_user(username):
        url = 'http://www.lydsy.com/JudgeOnline/userinfo.php?user={}'.format(username)
        res = HysbzHttp().get(url=url)
        return not re.findall(r"No such User!", res.text)
