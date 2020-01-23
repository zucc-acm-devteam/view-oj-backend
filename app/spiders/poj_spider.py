import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class PojSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://poj.org/userstatus?user_id={}'.format(username)
        res = SpiderHttp().get(url=url)
        accept_problem_list = re.findall(r'p\((\d+)\)', res.text)
        return accept_problem_list

    def get_problem_info(self, problem_id):
        url = 'http://poj.org/problem?id={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            total = int(re.search(r'<td><b>Total Submissions:</b> (\d+)</td>', res.text).group(1))
            accept = int(re.search(r'<td><b>Accepted:</b> (\d+)</td>', res.text).group(1))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'Hile_M'
    print(PojSpider().get_user_info(oj_username))
