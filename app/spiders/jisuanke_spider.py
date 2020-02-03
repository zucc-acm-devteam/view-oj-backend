import json
import re
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.models.mapping import Mapping
from app.spiders.base_spider import BaseSpider
from app.libs.spider_http import SpiderHttp


class JisuankeSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        username = oj_username.oj_username
        page = 1
        accept_problem_list = []
        success = False
        while True:
            url = 'https://i.jisuanke.com/timeline/nanti/{}?page={}'.format(username, page)
            res = SpiderHttp().get(url=url)
            try:
                res_json = json.loads(res.text)
            except:
                break
            success = True
            res = res_json.get('data', dict())
            if not res:
                break
            for data in res:
                problem_id = re.findall('//nanti.jisuanke.com/t/(.*)', data['url'])[0]
                problem_id = JisuankeSpider._change_problem_id(problem_id)
                accept_time = data['updated_at']
                if accept_problems.get('jisuanke-' + problem_id) == accept_time:
                    continue
                accept_problem_list.append({
                    'oj': 'jisuanke',
                    'problem_pid': problem_id,
                    'accept_time': accept_time
                })
            page += 1
        return {'success': success, 'data': accept_problem_list}

    def get_problem_info(self, problem_id):
        try:
            url = 'https://nanti.jisuanke.com/t/{}'.format(problem_id)
            res = SpiderHttp().get(url=url)
            data = re.findall(r'通过 (\d+) 人次 / 提交 (\d+) 人次', res.text)
            accept = int(data[0][0])
            total = int(data[0][1])
            rating = DEFAULT_PROBLEM_RATING

        except:
            rating = DEFAULT_PROBLEM_RATING

        return {'rating': rating}

    @staticmethod
    def _change_problem_id(problem_id):
        mapping = Mapping.get_by_id('jisuanke-{}'.format(problem_id))
        new_problem_id = mapping.value
        if new_problem_id:
            return new_problem_id
        res = SpiderHttp().get(url='http://nanti.jisuanke.com/t/{}'.format(problem_id))
        new_problem_id = re.findall(r'//nanti.jisuanke.com/t/(.*)', res.url)[0]
        mapping.modify(value=new_problem_id)
        return new_problem_id
