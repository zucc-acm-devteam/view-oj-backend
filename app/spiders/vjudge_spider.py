import json

from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class VjudgeSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        url = 'http://vjudge.net/user/solveDetail/{}'.format(username)
        res = SpiderHttp().post(url=url)
        res = json.loads(res.text)['acRecords']
        accept_problem_list = []
        for oj_name in res:
            for problem_id in res[oj_name]:
                accept_problem_list.append('{}-{}'.format(oj_name, problem_id))
        return accept_problem_list

    def get_problem_info(self, problem_id):
        pass


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'taoting'
    print(VjudgeSpider().get_user_info(oj_username))
