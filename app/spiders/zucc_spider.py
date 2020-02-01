import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.libs.spider_http import SpiderHttp


class ZuccHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'cookie': 'resolveIDs=0; order_dir_list_by=1A; PHPSESSID=ni7c6l5o3u2mgbl98d9ubi0fo5',
        }
        self.headers.update(headers)


class ZuccSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        if not self._judge_user(username):
            return {'success': False, 'data': []}
        accept_problem_list = []
        url = 'http://acm.zucc.edu.cn/status.php?user_id={}&jresult=4'.format(username)
        ok = False
        while not ok:
            res = ZuccHttp().get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            trs = soup.find('tbody').find_all('tr')
            if not trs:
                break
            for tr in trs:
                tds = tr.find_all('td')
                problem_id = tds[2].text
                accept_time = tds[8].text
                if accept_problems.get('zucc-' + problem_id) == accept_time:
                    ok = True
                    break
                accept_problem_list.append({
                    'oj': 'zucc',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
                next = int(tds[0].text)
            url = 'http://acm.zucc.edu.cn/status.php?user_id={}&jresult=4&top={}'.format(username,
                                                                                         next - 1)
        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        url = 'http://acm.zucc.edu.cn/problem.php?id={}'.format(problem_id)
        res = ZuccHttp().get(url=url)
        try:
            total = int(re.search(r'Submit: </span>(\d+)(&nbsp;)*<span', res.text).group(1))
            accept = int(re.search(r'Solved: </span>(\d+)(&nbsp;)*<br>', res.text).group(1))
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    @staticmethod
    def _judge_user(username):
        url = 'http://acm.zucc.edu.cn/userinfo.php?user={}'.format(username)
        res = ZuccHttp().get(url=url)
        return not re.findall(r"No such User!", res.text)
