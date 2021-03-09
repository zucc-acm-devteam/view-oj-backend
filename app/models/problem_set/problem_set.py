from sqlalchemy import Column, DateTime, Integer, String

from app.libs.error_code import NotFound
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
        from app.models.problem_set.problem_relationship import \
            ProblemRelationship
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
    def user_list(self):
        from app.models.problem_set.user_relationship import UserRelationship
        from app.models.user import User
        r = list()
        for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            r.append(User.get_by_id(i.username))
        return r

    @property
    def detail(self):
        from app.models.accept_problem import AcceptProblem
        from app.models.base import db
        from app.models.user import User
        query_res = db.session.query(User, AcceptProblem). \
            filter(User.username.in_([i.username for i in self.user_list])). \
            filter(AcceptProblem.username == User.username). \
            filter(AcceptProblem.problem_id.in_([i.id for i in self.problem_list])).all()
        res = {}
        for user in self.user_list:
            res.setdefault(user, [])
        for user, acp in query_res:
            res[user].append(acp)
        res = [{'user': i[0], 'data': i[1]} for i in res.items()]
        return res

    @classmethod
    def create(cls, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_set.problem_relationship import \
            ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        from app.models.user import User
        problem_set = super().create(**kwargs)
        for i in kwargs['problem_list']:
            oj_name, problem_pid = i['problem'].split('-', 1)
            oj = OJ.get_by_name(oj_name)
            problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
            ProblemRelationship.create(problem_id=problem.id, problem_set_id=problem_set.id, difficulty=i['difficulty'])
        for i in kwargs['user_list']:
            user = User.get_by_id(i)
            if user is None:
                continue
            UserRelationship.create(username=user.username, problem_set_id=problem_set.id)

    def modify(self, **kwargs):
        from app.models.oj import OJ
        from app.models.problem import Problem
        from app.models.problem_set.problem_relationship import \
            ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        from app.models.user import User
        if kwargs['problem_list'] is not None:
            for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
                i.delete()
            for i in kwargs['problem_list']:
                oj_name, problem_pid = i['problem'].split('-', 1)
                oj = OJ.get_by_name(oj_name)
                problem = Problem.get_by_oj_id_and_problem_pid(oj.id, problem_pid)
                ProblemRelationship.create(problem_id=problem.id, problem_set_id=self.id, difficulty=i['difficulty'])
            kwargs.pop('problem_list')
        if kwargs['user_list'] is not None:
            for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
                i.delete()
            for i in kwargs['user_list']:
                user = User.get_by_id(i)
                if user is None:
                    continue
                UserRelationship.create(username=user.username, problem_set_id=self.id)
            kwargs.pop('user_list')
        super().modify(**kwargs)

    def delete(self):
        from app.models.problem_set.problem_relationship import \
            ProblemRelationship
        from app.models.problem_set.user_relationship import UserRelationship
        for i in ProblemRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        for i in UserRelationship.search(problem_set_id=self.id, page_size=-1)['data']:
            i.delete()
        super().delete()
