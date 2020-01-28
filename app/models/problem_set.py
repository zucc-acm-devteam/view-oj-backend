from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class ProblemSet(Base):
    __tablename__ = 'problem_set'

    fields = ['id', 'name', 'problem_list', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    create_time = Column(DateTime)

    @property
    def problem_list(self):
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        r = list()
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=1000)['data']:
            r.append(Problem.get_by_id(i.problem_id))
        return r

    @classmethod
    def create(cls, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        problem_set = super().create(**kwargs)
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i.split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=problem_set.id)

    def modify(self, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        super().modify(**kwargs)
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=1000)['data']:
            i.delete()
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i.split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=self.id)
