import json
import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.libs.service import calculate_problem_rating
from app.models.mapping import get_value, set_value
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class JisuankeSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        page = 1
        accept_list = []
        while True:
            url = 'https://i.jisuanke.com/timeline/nanti/{}?page={}'.format(username, page)
            res = SpiderHttp().get(url=url)
            try:
                res_json = json.loads(res.text)
            except:
                break
            res = res_json.get('data',dict())
            if not res:
                break
            for data in res:
                problem_id = re.findall('//nanti.jisuanke.com/t/(.*)', data['url'])[0]
                problem_id = JisuankeSpider._change_problem_id(problem_id)
                accept_list.append(problem_id)
            page += 1
        return accept_list

    def get_problem_info(self, problem_id):
        try:
            url = 'https://nanti.jisuanke.com/t/{}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'通过 (\d+) 人次 / 提交 (\d+) 人次', res.text)
            accept = int(data[0][0])
            total = int(data[0][1])
            rating = int(calculate_problem_rating(total, accept))

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    @staticmethod
    def _change_problem_id(problem_id):
        new_problem_id = get_value('jisuanke-{}'.format(problem_id))
        if not new_problem_id:
            res = SpiderHttp().get(url='http://nanti.jisuanke.com/t/{}'.format(problem_id))
            new_problem_id = re.findall(r'//nanti.jisuanke.com/t/(.*)', res.url)[0]
            set_value('jisuanke-{}'.format(problem_id), new_problem_id)
        return new_problem_id


if __name__ == '__main__':
    from app.models.oj_username import OJUsername
    from app import create_app

    create_app().app_context().push()
    oj_username = OJUsername()
    oj_username.oj_username = '4lkvgc2'
    print(JisuankeSpider().get_user_info(oj_username))
