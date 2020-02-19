import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class PojSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        accept_problem_list = []
        url = 'http://poj.org/userstatus?user_id={}'.format(username)
        res = SpiderHttp().get(url=url)
        if "Sorry,{} doesn't exist".format(username) in res.text:
            return {'success': False, 'data': []}
        top = -1
        ok = False
        while not ok:
            url = 'http://poj.org/status?user_id={}&result=0&top={}'.format(username, top)
            res = SpiderHttp().get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            trs = soup.find_all('table')[-1].find_all('tr')[1:]
            if not trs:
                break
            for tr in trs:
                tds = tr.find_all('td')
                problem_id = tds[2].text
                accept_time = tds[8].text
                top = tds[0].text
                if accept_problems.get('poj-' + problem_id) == accept_time:
                    ok = True
                    break
                accept_problem_list.append({
                    'oj': 'poj',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })

        return {'success': True, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        url = 'http://poj.org/problem?id={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            total = int(re.search(r'<td><b>Total Submissions:</b> (\d+)</td>', res.text).group(1))
            accept = int(re.search(r'<td><b>Accepted:</b> (\d+)</td>', res.text).group(1))
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}
