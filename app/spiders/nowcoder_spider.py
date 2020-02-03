import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.libs.spider_http import SpiderHttp


class NowcoderSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        success = False
        uid = NowcoderSpider._get_id_by_username(username)
        if uid:
            username = uid
        index = 1
        accept_problem_list = []
        ok = False
        while not ok:
            url = 'http://ac.nowcoder.com/acm/contest/profile/{}/' \
                  'practice-coding?pageSize=200&statusTypeFilter=5&orderType=DESC&page={}'.format(
                username, index)
            res = SpiderHttp().get(url=url)
            if '用户不存在' in res.text:
                break
            if '没有找到你想要的内容呢' in res.text:
                break
            success = True
            soup = BeautifulSoup(res.text, 'lxml')
            trs = soup.find_all('tr')[1:]
            for tr in trs:
                tds = tr.find_all('td')
                accept_time = tds[8].text
                problem_id = re.findall(r'/acm/problem/(\d+)', tds[1].find('a')['href'])[0]
                if accept_problems.get('nowcoder-' + problem_id) == accept_time:
                    ok = True
                    break
                accept_problems['nowcoder-' + problem_id] = accept_time
                accept_problem_list.append({
                    'oj': 'nowcoder',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
            index += 1

        return {'success': success, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        star_rating = [DEFAULT_PROBLEM_RATING, 800, 1200, 1600, 2000, 2400]
        try:
            url = 'https://ac.nowcoder.com/acm/problem/list?keyword={}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'<td>\n(\d+)星\n</td>', res.text)
            star = int(data[0][0])
            rating = star_rating[star]
        except:
            rating = DEFAULT_PROBLEM_RATING
        return {'rating': rating}

    @staticmethod
    def _get_id_by_username(username):
        url = 'https://www.nowcoder.com/search?type=all&query={}'.format(username)
        res = SpiderHttp().get(url=url)
        result = re.findall(r'/profile/(\d+)', res.text)
        if not result:
            return None
        return result[0]

