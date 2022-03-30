from bs4 import BeautifulSoup
import time
import datetime

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.spider_http import SpiderHttp
from app.spiders.base_spider import BaseSpider


class AtcoderHttp(SpiderHttp):
    @staticmethod
    def _end_request(res, encoding: str):
        time.sleep(0.5)
        return res


class AtcoderSpider(BaseSpider):
    req = AtcoderHttp()

    def get_user_info(self, oj_username, accept_problems):  # 获取ac列表
        try:
            contest_list = self.get_contest_list(oj_username)
            accept_problem_list = []
            visited_id = []
            prefix = 'https://atcoder.jp'

            for i in contest_list:
                # print(i.get('name'))
                url = i.get('link')
                html = self.req.get(url=url)
                soup = BeautifulSoup(html.text, features='lxml')
                ul = soup.select('ul[class="pagination pagination-sm mt-0 mb-1"]')
                ul = ul[0]
                li = ul.select('li')
                length = len(li)
                mx = 0
                if length > 0:
                    mx = int(li[length - 1].select('a')[0].text)  # 获取页数
                for j in range(mx, 0, -1):
                    # print(str(j) + ' / ' + str(mx))
                    new_url = url + "&page=" + str(j)
                    html = self.req.get(url=new_url)
                    soup = BeautifulSoup(html.text, features='lxml')
                    tbody = soup.select('tbody')
                    tbody = tbody[0]
                    trs = tbody.select('tr')
                    trs.reverse()  # 从最开始的提交开始遍历

                    for tr in trs:  # 获取每一页的提交列表
                        td = tr.select('td')
                        state = td[6].select('span')[0].text  # 提交状态
                        accept_time = td[0].text  # 提交时间
                        pos = accept_time.find('+')  # 获取最后一个+的位置
                        if pos != -1:
                            accept_time = accept_time[0:pos]
                            accept_time = datetime.datetime.strptime(accept_time, '%Y-%m-%d %H:%M:%S')
                            accept_time = accept_time + datetime.timedelta(hours=-1)
                        else:
                            accept_time = datetime.datetime.strptime(accept_time, '%Y-%m-%d %H:%M:%S')
                        problem_link = prefix + td[1].select('a')[0].attrs['href']  # 题目链接
                        pos = problem_link.rfind('/')  # 获取最后一个/的位置
                        problem_pid = problem_link[(pos + 1):]  # 获取pid
                        if (state == 'AC') and (visited_id.count(problem_pid) == 0):
                            accept_problem_list.append({
                                'oj': 'atcoder',
                                'problem_pid': problem_pid,
                                'accept_time': accept_time.strftime('%Y-%m-%d %H:%M:%S'),
                            })
                            visited_id.append(problem_pid)
            return {'success': True, 'data': accept_problem_list}
        except:
            return {'success': False, 'data': []}

    def get_problem_info(self, problem_id):
        return {'rating': DEFAULT_PROBLEM_RATING}

    def get_contest_list(self, oj_username):  # 读取contest列表
        username = oj_username.oj_username
        url = "https://atcoder.jp/users/" + username + "/history"
        prefix = 'https://atcoder.jp'
        html = self.req.get(url=url)
        soup = BeautifulSoup(html.text, features="lxml")
        table = soup.select('#history')
        trs = []
        if len(table) > 0:
            trs = table[0].select('tr')

        contest_list = []

        for idx, tr in enumerate(trs):
            if idx == 0:
                continue
            td = tr.select('td')
            name = td[1].select('a')[0].text  # 比赛名称
            link = prefix + td[1].select('a')[1].attrs['href']  # 比赛链接
            contest_list.append({
                'name': name,
                'link': link
            })
        return contest_list