from urllib.parse import quote
from app.spiders.camp_spiders.base_camp_spider import BaseCampSpider
from app.libs.spider_http import SpiderHttp


class NowcoderCampSpider(BaseCampSpider):
    def get_user_info(self, contest_cid, course_oj_username):
        oj_username = course_oj_username.oj_username
        pass_list = set()
        rank = 0
        page = 1
        page_size = 1
        http = SpiderHttp()
        while page <= page_size:
            url = 'https://ac.nowcoder.com/acm-heavy/acm/contest/status-list' \
                  '?id={}&pageSize=20&statusTypeFilter=5&searchUserName' \
                  '={}&page={}'.format(contest_cid,
                                       quote(oj_username),
                                       page)
            res = http.get(url=url).json()
            if res['msg'] != 'OK':
                return {'success': False, 'data': None}
            for item in res['data']['data']:
                if item['userName'] == oj_username:
                    pass_list.add(item['index'])
            pass_list = list(pass_list)
            page_size = res['data']['basicInfo']['pageCount']
            page += 1
        url = 'https://ac.nowcoder.com/acm-heavy/acm/contest/' \
              'real-time-rank-data?id={}&' \
              'searchUserName={}'.format(contest_cid, quote(oj_username))
        res = http.get(url=url).json()
        if res['msg'] != 'OK':
            return {'success': False, 'data': None}
        for item in res['data']['rankData']:
            if item['userName'] == oj_username:
                rank = item['ranking']
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
