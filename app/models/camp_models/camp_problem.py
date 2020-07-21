from sqlalchemy import Column, ForeignKey, Integer, String

from app.models.base import Base
from app.models.camp_models.course_contest import CourseContest


class CampProblem(Base):
    __tablename__ = 'camp_problem'

    fields = ['id', 'contest_id', 'problem_pid']

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest_id = Column(Integer, ForeignKey(CourseContest.id))
    problem_pid = Column(String(100), nullable=False)

    @property
    def contest(self):
        return CourseContest.get_by_id(self.oj_id)

    @classmethod
    def get_by_contest_id_and_problem_pid(cls, contest_id, problem_pid):
        r = cls.search(contest_id=contest_id, problem_pid=problem_pid)['data']
        if r:
            return r[0]
        return cls.create(contest_id=contest_id, problem_pid=problem_pid)
