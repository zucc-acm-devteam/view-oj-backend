from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class ProblemSet(Base):
    __tablename__ = 'problem_set'

    fields = ['id', 'name', 'start_time', 'end_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    @property
    def problem_list(self):
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        r = list()
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            p = Problem.get_by_id(i.problem_id)
            p.difficulty = i.difficulty
            fields = Problem.fields.copy()
            fields.append('difficulty')
            p.fields = fields
            r.append(p)
        return r

    @property
    def detail(self):
        from app.models.accept_problem import AcceptProblem
        from app.models.base import db
        from app.models.user import User
        query_res = db.session.query(User, AcceptProblem). \
            filter(User.status == 1, User.is_freshman == 0). \
            filter(AcceptProblem.username == User.username). \
            filter(AcceptProblem.problem_id.in_([i.id for i in self.problem_list])).all()
        res = {}
        for user in User.search(status=1, is_freshman=0, page_size=-1)['data']:
            res.setdefault(user, [])
        for user, acp in query_res:
            res[user].append(acp)
        res = [{'user': i[0], 'data': i[1]} for i in res.items()]
        return res

    @classmethod
    def create(cls, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        problem_set = super().create(**kwargs)
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i['problem'].split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=problem_set.id, difficulty=i['difficulty'])

    def modify(self, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_relationship import ProblemRelationship
        if kwargs['problem_list'] is None:
            kwargs.pop('problem_list')
            super().modify(**kwargs)
            return
        super().modify(**kwargs)
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i['problem'].split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=self.id, difficulty=i['difficulty'])

    def delete(self):
        from app.models.problem_relationship import ProblemRelationship
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        super().delete()
