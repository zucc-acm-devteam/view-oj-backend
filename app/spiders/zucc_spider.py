import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class ZuccHttp(SpiderHttp):
    def __init__(self):
        super().__init__()
        headers = {
            'cookie': 'resolveIDs=0; order_dir_list_by=1A; PHPSESSID=ni7c6l5o3u2mgbl98d9ubi0fo5',
        }
        self.headers.update(headers)


class ZuccSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://acm.zucc.edu.cn/userinfo.php?user={}'.format(username)
        res = ZuccHttp().get(url=url)

        r = re.findall(r'p\((\d+),\d+\);', res.text)
        return r

    def get_problem_info(self, problem_id):
        url = 'http://acm.zucc.edu.cn/problem.php?id={}'.format(problem_id)
        res = ZuccHttp().get(url=url)

        try:
            total = int(re.search(r'Submit: </span>(\d+)(&nbsp;)*<span', res.text).group(1))
            accept = int(re.search(r'Solved: </span>(\d+)(&nbsp;)*<br>', res.text).group(1))
            rating = int(calculate_problem_rating(total, accept) * 0.8)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(ZuccSpider().get_problem_info('1962'))
