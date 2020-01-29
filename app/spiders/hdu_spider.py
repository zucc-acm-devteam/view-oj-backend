import json
import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class HduSpider(BaseSpider):
    @classmethod
    def get_user_info(cls, oj_username, accept_problems):
        username = oj_username.oj_username
        url = 'http://acm.hdu.edu.cn/status.php?user={}'.format(username)
        accept_problem_dict = {}
        finished = False
        while True:
            res = SpiderHttp().get(url=url)
            soup = BeautifulSoup(res.text, 'lxml')
            table = soup.find_all('table', {'class': 'table_text'})[0]
            trs = table.find_all('tr')[1:]
            for tr in trs:
                tds = tr.find_all('td')
                if tds[2].text == 'Accepted':
                    accept_time = tds[1].text
                    problem_pid = tds[3].text
                    if accept_problems.get('hdu-' + problem_pid) == accept_time:
                        finished = True
                        break
                    accept_problem_dict[problem_pid] = accept_time
            if finished:
                break
            next_page = soup.find('a', {'href': re.compile(r'.*first=[0-9].*')})
            if next_page:
                url = 'http://acm.hdu.edu.cn' + next_page['href']
            else:
                break
        accept_problem_list = [{
            'oj': 'hdu',
            'problem_pid': problem_pid,
            'accept_time': accept_time
        } for problem_pid, accept_time in accept_problem_dict.items()]
        return accept_problem_list

    @classmethod
    def get_problem_info(cls, problem_id):
        url = 'http://acm.hdu.edu.cn/showproblem.php?pid={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            re_res = re.search(r'<br>Total Submission\(s\): (\d+)(&nbsp;){4}Accepted Submission\(s\): (\d+)<br>',
                               res.text)
            total = int(re_res.group(1))
            accept = int(re_res.group(3))
            rating = DEFAULT_PROBLEM_RATING
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}
