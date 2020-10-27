import re
import time

from bs4 import BeautifulSoup

from app.libs.spider_http import SpiderHttp
from app.spiders.camp_spiders.base_camp_spider import BaseCampSpider


class HduHttp(SpiderHttp):
    @staticmethod
    def _before_request(url: str, params: dict, data: dict) -> (str, str):
        if 'userloginex.php' in url:
            time.sleep(10)
        return url, data


class HduCampSpider(BaseCampSpider):
    http = HduHttp()
    ranklist = []
    current_contest_cid = None

    def get_user_info(self, contest_cid, course_oj_username):
        oj_username = course_oj_username.oj_username
        if not self._check_login(contest_cid):
            try:
                self._login(contest_cid)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}
        pass_list = []
        url = 'http://acm.hdu.edu.cn/contests/contest_status.php?' \
              'cid={}&user={}&status=5'.format(contest_cid, oj_username)
        res = self.http.get(url=url)
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.text, 'lxml')
        trs = soup.find('table').find_all('tr')
        if len(trs) > 2:
            trs = trs[2:]
            for tr in trs:
                link = tr.find_all('a')[0]
                problem = link.text
                problem = chr(int(problem) - 1001 + ord('A'))
                pass_list.append(problem)
        pass_list = list(set(pass_list))
        rank = 0
        self._get_contest_ranklist()
        for i, item in enumerate(self.ranklist, 1):
            if item['name'] == oj_username:
                rank = i
        if rank == 0:
            return {'success': False, 'data': None}
        result = {
            'success': True,
            'data': {
                'pass_list': pass_list,
                'rank': rank
            }
        }
        return result

    def _login(self, contest_cid):
        self.current_contest_cid = contest_cid
        self.ranklist = []
        url = 'http://acm.hdu.edu.cn/userloginex.php?action=login&cid={}'.format(contest_cid)
        res = self.http.post(url=url, data={
            'username': self.username,
            'userpass': self.password,
        })
        if 'Sign In Your Account' in res.text:
            raise Exception('Login failed')
        url = 'http://acm.hdu.edu.cn/contests/' \
              'client_ranklist.php?cid={}'.format(self.current_contest_cid)
        res = self.http.get(url=url)
        res.encoding = 'gb2312'
        if 'c=' + self.current_contest_cid not in res.text:
            raise Exception('hdu bug')

    def _check_login(self, contest_cid):
        self.current_contest_cid = contest_cid
        url = 'http://acm.hdu.edu.cn/contests/contest_show.php?cid={}'.format(contest_cid)
        res = self.http.get(url=url)
        return 'Sign In Your Account' not in res.text

    def _get_contest_ranklist(self):
        # need to check login first
        if self.ranklist:
            return
        url = 'http://acm.hdu.edu.cn/contests/' \
              'client_ranklist.php?cid={}'.format(self.current_contest_cid)
        res = self.http.get(url=url)
        res.encoding = 'gb2312'
        if 'c=' + self.current_contest_cid not in res.text:
            raise Exception('hdu bug')
        res = re.findall(r'pr\((.*)\)', res.text)[1:]
        ranklist = []
        for item in res:
            splited = item.split(',')
            ranklist.append({
                'passed': int(splited[3]),
                'name': splited[2][1:-1]
            })
        self.ranklist = ranklist
        return

    def get_contest_meta(self, contest_cid):
        if not self._check_login(contest_cid):
            try:
                self._login(contest_cid)
            except Exception as e:
                print(e)
                return {'success': False, 'data': None}
        url = 'http://acm.hdu.edu.cn/contests/contest_show.php?cid={}'.format(contest_cid)
        res = self.http.get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        table = soup.find('table')
        trs = table.find_all('tr')[1:]
        problems = [chr(ord('A') + i) for i in range(0, len(trs))]
        self._get_contest_ranklist()
        max_pass = self.ranklist[0]['passed']
        participants = len(self.ranklist)
        return {
            'success': True,
            'data': {
                'max_pass': max_pass,
                'participants': participants,
                'problems': problems
            }
        }
