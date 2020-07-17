from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class ProblemSet(Base):
    __tablename__ = 'problem_set'

    fields = ['id', 'name']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    @property
    def problem_list(self):
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        r = list()
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            r.append(Problem.get_by_id(i.problem_id))
        return r

    @property
    def detail(self):
        from app.models.accept_problem import AcceptProblem
        from app.models.user import User
        res = []
        user_list = User.search(status=1, page_size=-1)['data']
        for i in user_list:
            res.append({
                'user': i,
                'data': AcceptProblem.query.filter(
                    AcceptProblem.username == i.username,
                    AcceptProblem.problem_id.in_([i.id for i in self.problem_list])).all()
            })
        return res

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
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i.split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=self.id)

    def delete(self):
        from app.models.problem_relationship import ProblemRelationship
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        super().delete()