from abc import ABCMeta, abstractmethod

from app.models.oj_username import OJUsername


class BaseSpider(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_user_info(cls, oj_username: OJUsername, accept_problems: dict) -> dict:
        """
        获取用户信息
        :param oj_username: OJUsername对象
        :param accept_problems: 通过的题目的字典
        {"hdu-1000": "2019-01-01 12:12:12", "hdu-1001": "2019-01-01 12:12:13"}
        :return 结果字典
        {
            "success": True, # 是否成功
            "data":[ # 题目列表
                {"oj": "hdu", "problem_pid": "1000", "accept_time": "2019-01-01 12:12:12"},
                {"oj": "hdu", "problem_pid": "1001", "accept_time": None}
            ]
        }
        """
        pass

    @classmethod
    @abstractmethod
    def get_problem_info(cls, problem_pid):
        """
        获取用户信息
        :param problem_pid: 题目pid
        :return 题目信息
        {"rating": 1500}
        """
        pass
