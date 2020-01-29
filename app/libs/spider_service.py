import datetime

from app.models.accept_problem import AcceptProblem
from app.models.oj import OJ
from app.models.oj_username import OJUsername
from app.models.problem import Problem
from app.spiders.base_spider import BaseSpider
# 导入spider
from app.spiders.codeforces_spider import CodeforcesSpider


# from app.spiders.hdu_spider import HduSpider
# from app.spiders.hysbz_spider import HysbzSpider
# from app.spiders.jisuanke_spider import JisuankeSpider
# from app.spiders.loj_spider import LojSpider
# from app.spiders.luogu_spider import LuoguSpider
# from app.spiders.nit_spider import NitSpider
# from app.spiders.nowcoder_spider import NowcoderSpider
# from app.spiders.pintia_spider import PintiaSpider
# from app.spiders.poj_spider import PojSpider
# from app.spiders.vjudge_spider import VjudgeSpider
# from app.spiders.zoj_spider import ZojSpider
# from app.spiders.zucc_spider import ZuccSpider


def crawl_accept_problem(username, oj_id):
    oj_name = OJ.get_by_id(oj_id).name
    oj_username = OJUsername.search(username=username, oj_id=oj_id)['data']
    if not oj_username:
        return

    oj_username = oj_username[0]
    oj_spider: BaseSpider = globals()[oj_name.title() + 'Spider']

    accept_problems = dict()

    for i in AcceptProblem.search(username=username)['data']:
        accept_problems["{}-{}".format(i.problem.oj.name, i.problem.problem_pid)] = \
            datetime.datetime.strftime(i.create_time, '%Y-%m-%d %H:%M:%S')

    crawl_accept_problems = oj_spider.get_user_info(oj_username, accept_problems)

    deduplication_accept_problem = list()

    for i in crawl_accept_problems:
        pid = "{}-{}".format(i['oj'], i['problem_pid'])
        if i['accept_time'] is not None:
            if accept_problems.get(pid):
                if i['accept_time'] < accept_problems.get(pid):
                    deduplication_accept_problem.append(i)
            else:
                deduplication_accept_problem.append(i)
        else:
            if accept_problems.get(pid) is None:
                deduplication_accept_problem.append(i)

    for i in deduplication_accept_problem:
        oj = OJ.get_by_name(i['name'])
        problem = Problem.get_by_oj_id_and_problem_pid(oj.id, i['problem_pid'])
        accept_problem = AcceptProblem.get_by_username_and_problem_id(username, problem.id)
        accept_problem.modify(create_time=i['accept_time'])


if __name__ == '__main__':
    from app import create_app

    create_app().app_context().push()

    crawl_accept_problem('admin', 2)
