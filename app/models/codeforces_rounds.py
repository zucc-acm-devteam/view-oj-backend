from sqlalchemy import (Column, Date, DateTime, ForeignKey, Integer, String,
                        cast, func)

import datetime
from app.models.base import Base, db
from app.models.user import User


class CodeforcesRounds(Base):
    __tablename__ = 'codeforces_rounds'
    fields = ['id', 'username', 'round_name', 'rating_change', 'create_time']

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), ForeignKey(User.username))
    round_name = Column(String(100), nullable=False)
    rank = Column(Integer, nullable=False)
    rating_change = Column(Integer, nullable=False)
    create_time = Column(DateTime, nullable=False)

    @classmethod
    def get_by_username_and_round_name(cls, username, round_name):
        r = cls.search(username=username, round_name=round_name)['data']
        if r:
            return r[0]
        return cls.create(username=username, round_name=round_name, rank=0, rating_change=0)

    @staticmethod
    def search_distribute(username, start_date, end_date):
        r = dict()
        for i in db.session.query(cast(CodeforcesRounds.create_time, Date),
                                  func.count(CodeforcesRounds.rating_change)).filter(
            CodeforcesRounds.username == username,
            CodeforcesRounds.create_time >= start_date,
            CodeforcesRounds.create_time < end_date + datetime.timedelta(days=1)
        ).group_by(cast(CodeforcesRounds.create_time, Date)).all():
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
