from urllib.parse import quote
from app.spiders.camp_spiders.base_camp_spider import BaseCampSpider
from app.libs.spider_http import SpiderHttp


class NowcoderCampSpider(BaseCampSpider):
    def get_user_info(self, contest_cid, course_oj_username):
        oj_username = course_oj_username.oj_username
        pass_list = []
        rank = 0
        http = SpiderHttp()
        url = 'https://ac.nowcoder.com/acm-heavy/acm/contest/' \
              'real-time-rank-data?id={}&' \
              'searchUserName={}'.format(contest_cid, quote(oj_username))
        res = http.get(url=url).json()
        if res['msg'] != 'OK':
            return {'success': False, 'data': None}
        problem_dict = {}
        for problem_info in res['data']['problemData']:
            problem_dict[problem_info['problemId']] = problem_info['name']
        for item in res['data']['rankData']:
            if item['userName'] != oj_username:
                continue
            rank = item['ranking']
            for problem_info in item['scoreList']:
                if not problem_info['accepted']:
                    continue
                pass_list.append(problem_info['problemId'])
        if rank == 0:
            return {'success': False, 'data': None}
        result = {
            'success': True,
            'data': {
                'pass_list': pass_list,
                'rank': rank
            }
        }
        return result

    def get_contest_meta(self, contest_cid):
        url = 'https://ac.nowcoder.com/acm-heavy/acm/contest/' \
              'real-time-rank-data?id={}'.format(contest_cid)
        res = SpiderHttp().get(url=url).json()
        if res['msg'] != 'OK':
            return {'success': False, 'data': None}
        max_pass = res['data']['rankData'][0]['acceptedCount']
        participants = res['data']['basicInfo']['rankCount']
        problems = [i['name'] for i in res['data']['problemData']]
        return {
            'success': True,
            'data': {
                'max_pass': max_pass,
                'participants': participants,
                'problems': problems
            }
        }
