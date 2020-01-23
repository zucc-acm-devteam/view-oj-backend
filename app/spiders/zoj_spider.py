import json
import re

from parsel import Selector

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class ZojSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://new.npuacm.info/api/crawlers/zoj/{}'.format(username)
        res = SpiderHttp().get(url=url)
        res_json = json.loads(res.text)
        return res_json.get('data', dict()).get('solvedList', list())

    def get_problem_info(self, problem_id):
        problem_id = int(problem_id) - 1000
        url = 'http://acm.zju.edu.cn/onlinejudge/showProblemStatus.do?problemId={}'.format(problem_id)
        res = SpiderHttp().get(url=url)

        try:
            selector = Selector(res.text)
            total = int(selector.xpath('//*[@id="content_body"]/div[2]/table/tr[2]/td[10]/a/text()').get())
            accept_tmp = selector.xpath('//*[@id="content_body"]/div[2]/table/tr[2]/td[1]/a/text()').get()
            accept = int(re.search(r'(\d+)\(\d+%+\)', accept_tmp).group(1))
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    print(ZojSpider().get_problem_info('1001'))
