from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Problem(Base):
    __tablename__ = 'problem'

    id = Column(Integer, primary_key=True, autoincrement=True)
    oj_id = Column(Integer, nullable=False)
    problem_pid = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)

    @property
    def url(self):
        try:
            if self.oj.name == 'codeforces':
                import re
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
