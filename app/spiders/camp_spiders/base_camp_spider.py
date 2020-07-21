from abc import ABCMeta, abstractmethod

from app.models.camp_models.course_oj_username import CourseOJUsername


class BaseCampSpider(metaclass=ABCMeta):
    def __init__(self, spider_info=None):
        """
        :param spider_info:{
            "username": "test1",
            "password": "test"
        }
        """
        if spider_info is None:
            return
        self.username = spider_info['username']
        self.password = spider_info['password']
        super().__init__()

    @abstractmethod
    def get_user_info(self, contest_cid: str, course_oj_username: CourseOJUsername) -> dict:
        """
        获取用户信息
        :param contest_cid: cid
        :param course_oj_username: OJUsername对象
        :return 结果字典
        {
            "success": True, # 是否成功
            "data":{
                "pass_list": [ "A", "C" ], # 题目列表
                "rank": 1
            }
        }
        """
        pass

    @abstractmethod
    def get_contest_meta(self, contest_cid: str):
        """
        :return:
        {
            "success": True,
            "data":{
                "max_pass": 5,
                "participants": 12,
                "problems": ["A","B","C1","C2",...]
            }
        }
        """
        pass
