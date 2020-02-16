import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, cast, Date, func

from app.models.base import Base, db
from app.models.problem import Problem
from app.models.user import User


class AcceptProblem(Base):
    __tablename__ = 'accept_problem'

    fields = ['id', 'username', 'problem_id', 'problem', 'add_rating', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    problem_id = Column(Integer, ForeignKey(Problem.id))
    add_rating = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

    @property
    def problem(self):
        return Problem.get_by_id(self.problem_id)

    @classmethod
    def get_by_username_and_problem_id(cls, username, problem_id):
        r = cls.search(username=username, problem_id=problem_id)['data']
        if r:
            return r[0]
        return cls.create(username=username, problem_id=problem_id, add_rating=0)

    @staticmethod
    def search_distribute(username, start_date, end_date):
        r = dict()
        for i in db.session.query(cast(AcceptProblem.create_time, Date), func.count(AcceptProblem.add_rating)).filter(
                AcceptProblem.username == username,
                AcceptProblem.create_time >= start_date,
                AcceptProblem.create_time < end_date + datetime.timedelta(days=1)
        ).group_by(cast(AcceptProblem.create_time, Date)).all():
            r[i[0].strftime('%Y-%m-%d %H:%M:%S')] = int(i[1])
        res = []
        while 1:
            if start_date > end_date:
                break
            res.append({
                'date': start_date,
                'count': r.get(start_date.strftime('%Y-%m-%d %H:%M:%S'), 0)
            })
            start_date += datetime.timedelta(days=1)
        return res
