import re

from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.oj import OJ


class Problem(Base):
    __tablename__ = 'problem'

    fields = ['id', 'oj_id', 'oj', 'problem_pid', 'rating', 'url']

    id = Column(Integer, primary_key=True, autoincrement=True)
    oj_id = Column(Integer, ForeignKey(OJ.id))
    problem_pid = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)

    @property
    def oj(self):
        return OJ.get_by_id(self.oj_id)

    @property
    def url(self):
        try:
            if self.oj.name == 'codeforces':
                p = re.match('^([0-9]+)([a-zA-Z]+[0-9]*)$', self.problem_pid)
                problem_id_1 = p.group(1)
                problem_id_2 = p.group(2)
                if int(problem_id_1) < 100000:
                    return "https://codeforces.com/problemset/problem/{}/{}".format(problem_id_1, problem_id_2)
                else:
                    return "https://codeforces.com/gym/{}/problem/{}".format(problem_id_1, problem_id_2)

            return self.oj.url.format(self.problem_pid)
        except:
            return None

    @classmethod
    def get_by_oj_id_and_problem_pid(cls, oj_id, problem_pid):
        r = cls.search(oj_id=oj_id, problem_pid=problem_pid)['data']
        if r:
            return r[0]
        return cls.create(oj_id=oj_id, problem_pid=problem_pid)
