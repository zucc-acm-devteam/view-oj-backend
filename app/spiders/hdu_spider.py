import json
import re

from bs4 import BeautifulSoup

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class HduSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://acm.hdu.edu.cn/userstatus.php?user={}'.format(username)
        res = SpiderHttp().get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        res = soup.findAll('p', {'align': 'left'})[0]
        return re.findall(r'p\((\d+).*?\);', res.text)

    def get_problem_info(self, problem_id):
        url = 'http://acm.hdu.edu.cn/showproblem.php?pid={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            re_res = re.search(r'<br>Total Submission\(s\): (\d+)(&nbsp;){4}Accepted Submission\(s\): (\d+)<br>',
                               res.text)
            total = int(re_res.group(1))
            accept = int(re_res.group(3))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'sumingzeng'
    print(HduSpider().get_user_info(oj_username))
