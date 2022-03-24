from sqlalchemy import create_engine

from app.config.secure import JIUDGE_DATABASE_URI
from app.config.setting import DEFAULT_PROBLEM_RATING
from app.spiders.base_spider import BaseSpider


class JiudgeSpider(BaseSpider):
    def get_user_info(self, oj_username, accept_problems):
        try:
            db = create_engine(JIUDGE_DATABASE_URI)
            res = db.execute('''
            select oj.name oj_name, remote_problem_id, submit_time
                from submission,
                     problem,
                     oj
            where problem.id = submission.problem_id
                and problem.oj_id = oj.id
                and submission.result in (select * from acceptable_results)
                and username = %s
            order by submit_time desc
            ''', oj_username.oj_username).fetchall()
            accept_problem_list = []
            exclude_oj = ['zucc-domjudge', 'zju-domjudge']
            for oj_name, problem_pid, accept_time in res:
                if oj_name in exclude_oj:
                    continue
                accept_problem_list.append({
                    'oj': oj_name,
                    'problem_pid': problem_pid,
                    'accept_time': accept_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            return {'success': True, 'data': accept_problem_list}
        except:
            return {'success': False, 'data': []}

    def get_problem_info(self, problem_pid):
        return {'rating': DEFAULT_PROBLEM_RATING}
