import re

from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider
from app.spiders.spider_http import SpiderHttp


class NowcoderSpider(BaseSpider):
    def get_user_info(self, oj_username):
        username = oj_username.oj_username
        uid = NowcoderSpider._get_id_by_username(username)
        if uid:
            username = uid
        index = 1
        data = []
        pre = []
        while 1:
            url = 'https://ac.nowcoder.com/acm/contest/profile/{}/practice-coding?pageSize=200&statusTypeFilter=5&page={}'.format(
                username, index)
            res = SpiderHttp().get(url=url)
            r = re.findall(r'/acm/problem/(\d+)', res.text)
            if r == pre:
                break
            data.extend(r)
            pre = r
            index += 1

        return data

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
        test = re.findall(r'/profile/(\d+)', res.text)
        if not test:
            return None
        return test[0]


if __name__ == '__main__':
    from app.models.oj_username import OJUsername

    oj_username = OJUsername()
    oj_username.oj_username = 'Kwords'
    print(NowcoderSpider().get_user_info(oj_username))
