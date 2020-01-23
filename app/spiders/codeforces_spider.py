import json
import re

from bs4 import BeautifulSoup

import app.models.mapping as mapping
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class CodeforcesSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        accept_problem_list = []
        url = 'http://codeforces.com/api/user.status?handle={}'.format(username)
        res = SpiderHttp().get(url=url)
        res = json.loads(res.text)
        if res['status'] != 'OK':
            return []
        res = res['result']
        for rec in res:
            if rec['verdict'] == 'OK':
                accept_problem_list.append('{}-{}'.format(rec['problem']['contestId'], rec['problem']['index']))
        return accept_problem_list

    def get_problem_info(self, problem_id):
        p = re.match('^([0-9]+)([a-zA-Z]+[0-9]*)$', problem_id)
        problem_id_1 = p.group(1)
        problem_id_2 = p.group(2)
        if int(problem_id_1) < 100000:  # 题目
            url = 'https://codeforces.com/problemset/problem/{}/{}'.format(problem_id_1, problem_id_2)
            res = SpiderHttp().get(url=url)
            try:
                rating = int(re.search(r'title="Difficulty">\s*\*(\d+)\s*</span>', res.text).group(1))
            except:
                rating = DEFAULT_PROBLEM_RATING
        else:  # gym
            try:
                rating = self._get_gym_constest_rating(problem_id_1)
            except:
                rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_gym_constest_rating(contest_id):
        star_rating = [DEFAULT_PROBLEM_RATING, 1200, 1600, 2000, 2400, 2800]
        stars = mapping.get_value('gym-{}'.format(contest_id))
        if stars is not None:
            return star_rating[int(stars)]
        url = 'https://codeforces.com/gyms'
        req = SpiderHttp()
        res = req.get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        token = soup.find('input', {'name': 'csrf_token'})['value']
        res = req.post(url=url, data={
            'csrf_token': token,
            'searchByNameOrIdQuery': contest_id,
            'searchByProblem': False,
        })
        soup = BeautifulSoup(res.text, 'lxml')
        stars = len(soup.find('tr', {'data-contestid': contest_id}).findAll('img'))
        mapping.set_value('gym-{}'.format(contest_id), str(stars))
        return star_rating[stars]


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'StupidTurtle'
    print(CodeforcesSpider().get_user_info(oj_username))
