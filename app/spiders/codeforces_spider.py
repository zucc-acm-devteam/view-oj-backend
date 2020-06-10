import json
import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.helper import timestamp_to_str
from app.libs.spider_http import SpiderHttp
from app.models.mapping import Mapping
from app.models.user import User
from app.spiders.base_spider import BaseSpider


class CodeforcesSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        rating = self.get_rating(username)
        contest_num = self.get_contest_num(username)
        user = User.get_by_id(oj_username.username)
        user.modify(codeforces_rating=rating, contest_num=contest_num)

        accept_problem_list = []
        url = 'http://codeforces.com/api/user.status?handle={}'.format(username)
        res = SpiderHttp().get(url=url)
        res = json.loads(res.text)
        if res['status'] != 'OK':
            return {'success': False, 'data': []}
        res = res['result']
        success = False
        for rec in res:
            success = True
            if rec['testset'] == 'PRETESTS':
                continue
            if rec.get('verdict') == 'OK':
                if rec['problem'].get('problemsetName'):
                    problem_pid = rec['problem']['index']
                else:
                    problem_pid = '{}{}'.format(rec['problem']['contestId'], rec['problem']['index'])
                accept_time = timestamp_to_str(rec['creationTimeSeconds'])
                if accept_problems.get("codeforces-{}".format(problem_pid)) == accept_time:
                    break
                accept_problem_list.append({
                    'oj': 'codeforces',
                    'problem_pid': problem_pid,
                    'accept_time': accept_time
                })
        return {'success': success, 'data': accept_problem_list}

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
                rating = self._get_gym_contest_rating(problem_id_1)
            except:
                rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_gym_contest_rating(contest_id):
        star_rating = [DEFAULT_PROBLEM_RATING, 1200, 1600, 2000, 2400, 2800]
        mapping = Mapping.get_by_id('gym-{}'.format(contest_id))
        stars = mapping.value
        if stars:
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
        mapping.modify(value=str(stars))
        return star_rating[stars]

    @staticmethod
    def get_rating(username):
        url = 'http://codeforces.com/api/user.info?handles={}'.format(username)
        res = SpiderHttp().get(url=url).json()
        return res['result'][0]['rating']

    @staticmethod
    def get_contest_num(username):
        url = 'http://codeforces.com/api/user.rating?handle={}'.format(username)
        res = SpiderHttp().get(url=url).json()
        return len(res['result'])
