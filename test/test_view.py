import json
from test.base import BaseTest


class ViewTest(BaseTest):
    def get_session(self):
        res = self.test_client.get('/v2/session')
        return json.loads(res.data)

    def create_session(self, username, password):
        res = self.test_client.post('/v2/session', json={
            'username': username,
            'password': password
        })
        return json.loads(res.data)

    def delete_session(self):
        res = self.test_client.delete('/v2/session')
        return json.loads(res.data)

    def test_session(self):
        # 获取登录状态
        self.assertFalse(self.get_session()['code'] == 0)
        # 管理员登录
        self.assertTrue(self.create_session('admin', 'admin')['code'] == 0)
        # 获取登录状态
        self.assertTrue(self.get_session()['data']['username'] == 'admin')
        # 管理员登出
        self.assertTrue(self.delete_session()['code'] == 0)

        # 获取登录状态
        self.assertFalse(self.get_session()['code'] == 0)
        # 普通用户登录
        self.assertTrue(self.create_session('user', 'user')['code'] == 0)
        # 获取登录状态
        self.assertTrue(self.get_session()['data']['username'] == 'user')
        # 普通用户登出
        self.assertTrue(self.delete_session()['code'] == 0)

        # 获取登录状态
        self.assertFalse(self.get_session()['code'] == 0)

    def get_user(self, id_):
        res = self.test_client.get('/v2/user/{}'.format(id_))
        return json.loads(res.data)

    def create_user(self, id_):
        res = self.test_client.post('/v2/user', json={
            'username': id_
        })
        return json.loads(res.data)

    def modify_user(self, id_, **kwargs):
        res = self.test_client.patch('/v2/user/{}'.format(id_), json=kwargs)
        return json.loads(res.data)

    def search_user(self):
        res = self.test_client.get('/v2/user')
        return json.loads(res.data)

    def test_user(self):
        # 普通用户登录
        self.assertTrue(self.create_session('user', 'user')['code'] == 0)
        # 获取当前用户信息
        self.assertTrue(self.get_user('user')['data']['username'] == 'user')
        # 获取其他用户信息(reject)
        self.assertFalse(self.get_user('admin')['code'] == 0)
        # 修改当前用户信息
        self.assertTrue(self.modify_user('user', nickname='user123')['code'] == 0)
        # 获取当前用户信息
        self.assertTrue(self.get_user('user')['data']['nickname'] == 'user123')
        # 修改当前用户敏感信息(reject)
        self.assertFalse(self.modify_user('admin', status=1)['code'] == 0)
        # 获取当前用户信息
        self.assertTrue(self.get_user('user')['data']['status'] == 0)
        # 修改其他用户信息(reject)
        self.assertFalse(self.modify_user('admin', nickname='user123')['code'] == 0)
        # 普通用户登出
        self.assertTrue(self.delete_session()['code'] == 0)

        # 管理员登录
        self.assertTrue(self.create_session('admin', 'admin')['code'] == 0)
        # 获取当前用户信息
        self.assertTrue(self.get_user('admin')['data']['username'] == 'admin')
        # 获取其他用户信息
        self.assertTrue(self.get_user('user')['data']['username'] == 'user')
        # 修改其他用户信息
        self.assertTrue(self.modify_user('user', nickname='user111')['code'] == 0)
        # 获取其他用户信息
        self.assertTrue(self.get_user('user')['data']['nickname'] == 'user111')
        # 修改其他用户敏感信息
        self.assertTrue(self.modify_user('user', status=1)['code'] == 0)
        # 获取其他用户信息
        self.assertTrue(self.get_user('user')['data']['status'] == 1)
        # 获取所有用户信息
        self.assertTrue(len(self.search_user()['data']['data']) == 2)
        # 创建用户
        self.assertTrue(self.create_user('guest')['code'] == 0)
        # 获取创建的用户信息
        self.assertTrue(self.get_user('guest')['data']['nickname'] == 'guest')
        # 获取所有用户信息
        self.assertTrue(len(self.search_user()['data']['data']) == 3)
        # 管理员登出
        self.assertTrue(self.delete_session()['code'] == 0)

    def create_oj_username(self, username, oj_id, oj_username):
        res = self.test_client.post('/v2/oj_username', json={
            'username': username,
            'oj_id': oj_id,
            'oj_username': oj_username
        })
        return json.loads(res.data)

    def search_oj_username(self, **kwargs):
        res = self.test_client.get('/v2/oj_username')
        return json.loads(res.data)

    def test_oj_username(self):
        # 普通用户登录
        self.assertTrue(self.create_session('user', 'user')['code'] == 0)
        pass
