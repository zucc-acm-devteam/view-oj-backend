import datetime
import json
import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.models.mapping import Mapping
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class CodeforcesSpider(BaseSpider):
    @classmethod
    def get_user_info(cls, oj_username, accept_problems):
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
                problem_pid = '{}-{}'.format(rec['problem']['contestId'], rec['problem']['index'])
                accept_time = datetime.datetime.strftime(
                    datetime.datetime.fromtimestamp(rec['creationTimeSeconds']), '%Y-%m-%d %H:%M:%S')
                if accept_problems.get(problem_pid) == accept_time:
                    break
                accept_problem_list.append({
                    'oj': 'codeforces',
                    'problem_pid': problem_pid,
                    'accept_time': accept_time
                })
        return accept_problem_list

    @classmethod
    def get_problem_info(cls, problem_id):
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
                rating = cls._get_gym_contest_rating(problem_id_1)
            except:
                rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_gym_contest_rating(contest_id):
        star_rating = [DEFAULT_PROBLEM_RATING, 1200, 1600, 2000, 2400, 2800]
        stars = Mapping.get_by_id('gym-{}'.format(contest_id))
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
        Mapping.create(key='gym-{}'.format(contest_id), value=str(stars))
        return star_rating[stars]
