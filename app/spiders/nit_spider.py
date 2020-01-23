import json
import re

from bs4 import BeautifulSoup
from parsel import Selector

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class NitSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'https://www.nitacm.com/userinfo.php?name={}'.format(username)
        res = SpiderHttp().get(url=url)
        soup = BeautifulSoup(res.text, 'lxml')
        raw_data = []
        for i in soup.find(id='userac'):
            try:
                raw_data.append(i.text)
            except AttributeError:
                pass
        data = []
        for i in raw_data:
            r = self._get_problem_info(i)
            data.append(r)
        return data

    def _get_problem_info(self, problem_id):
        url = 'https://www.nitacm.com/problem_show.php?pid={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            selector = Selector(res.text)
            oj_name = selector.xpath('//*[@id="conditions"]/span[1]/text()').get()
            remote_problem_id = selector.xpath('//*[@id="conditions"]/a/text()').get()
            if remote_problem_id:
                return oj_name + "-" + remote_problem_id
            return "nit-" + problem_id
        except:
            return "nit-" + problem_id

    def get_problem_info(self, problem_id):
        url = 'https://www.nitacm.com/problem_stat.php?pid={}'.format(problem_id)
        res = SpiderHttp().get(url=url)
        try:
            selector = Selector(res.text)
            total = int(selector.xpath('//*[@id="probstat"]/tbody/tr[1]/td/a/text()').get())
            accept = int(selector.xpath('//*[@id="probstat"]/tbody/tr[2]/td/a/text()').get())
            rating = calculate_problem_rating(total, accept)
        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'taoting'
    print(NitSpider().get_user_info(oj_username))
