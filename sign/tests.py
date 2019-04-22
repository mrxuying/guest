##该文件不能单独执行**

##以下是实现外部调用Django内部模块的方法，
# import os
# import sys
# import django
# sys.path.append(r'C:\git_project\guest')
# os.chdir(r'C:\git_project\guest')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guest.settings")
# django.setup()

# print(Event.objects.all())
# print(Guest.objects.all())    ##for test
##---------------------------------------------分割线-------------------------------------------
from django.test import TestCase
from sign.models import Event,Guest
from django,contrib.auth.models import User

# Create your tests here.

class ModuleTest(TestCase):
    def setUp(self):
        #增加发布会
        Event.objects.create(id=3, name='xiaomi 9 event', status=True, limit=2000, address='wuhan', start_time='2019-03-01 14:00:00')
        #新增一个嘉宾
        Guest.objects.create(id=1, event_id=3,realname='Alen', phone='18989898989', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='xiaomi 9 event')
        self.assertEqual(result.address,'wuhan')
        self.assertEqual(result.address,'wuhan')

    def test_guest_models(self):
        result = Guest.objects.get(phone='18989898989')
        self.assertEqual(result.realname,'Alen')
        self.assertFalse(result.sign)

class TestLogin(TestCase):
    '''测试登录首页'''
    def test_index_page(self):
        response = self.client.get('index')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')##断言响应的模板是否为‘index。html’

class TestLoginAction(TestCase):
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com','admin123')

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username,'admin')
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        ''' 用户名密码为空 '''
        response = self.client.post('/login_action/', {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password null!", response.content)

    def test_login_action_username_password_error(self):
        ''' 用户名密码错误 '''
        response = self.client.post('/login_action/', {'username': 'abc', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"username or password error!", response.content)

    def test_login_action_success(self):
        ''' 登录成功 '''
        response = self.client.post('/login_action/', data={'username': 'admin', 'password': 'admin123456'})
        self.assertEqual(response.status_code, 302)


class EventMangeTest(TestCase):
    ''' 发布会管理 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_add_event_data(self):
        ''' 测试添加发布会 '''
        event = Event.objects.get(name="xiaomi5")
        self.assertEqual(event.address, "beijing")

    def test_event_mange_success(self):
        ''' 测试发布会:xiaomi5 '''
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)

    def test_event_mange_search_success(self):
        ''' 测试发布会搜索 '''
        response = self.client.post('/search_name/', {"name": "xiaomi5"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"xiaomi5", response.content)
        self.assertIn(b"beijing", response.content)


class GuestManageTest(TestCase):
    ''' 嘉宾管理 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1,name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        Guest.objects.create(realname="alen", phone=18611001100,email='alen@mail.com', sign=0, event_id=1)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_add_guest_data(self):
        ''' 测试添加嘉宾 '''
        guest = Guest.objects.get(realname="alen")
        self.assertEqual(guest.phone, "18611001100")
        self.assertEqual(guest.email, "alen@mail.com")
        self.assertFalse(guest.sign)

    def test_event_mange_success(self):
        ''' 测试嘉宾信息: alen '''
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)

    def test_guest_mange_search_success(self):
        ''' 测试嘉宾搜索 '''
        response = self.client.post('/search_phone/',{"phone":"18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"alen", response.content)
        self.assertIn(b"18611001100", response.content)


class SignIndexActionTest(TestCase):
    ''' 发布会签到 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Event.objects.create(id=1, name="xiaomi5", limit=2000, address='beijing', status=1, start_time='2017-8-10 12:30:00')
        Event.objects.create(id=2, name="oneplus4", limit=2000, address='shenzhen', status=1, start_time='2017-6-10 12:30:00')
        Guest.objects.create(realname="alen", phone=18611001100, email='alen@mail.com', sign=0, event_id=1)
        Guest.objects.create(realname="una", phone=18611001101, email='una@mail.com', sign=1, event_id=2)
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)

    def test_sign_index_action_phone_null(self):
        ''' 手机号为空 '''
        response = self.client.post('/sign_index_action/1/', {"phone": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"phone error.", response.content)

    def test_sign_index_action_phone_or_event_id_error(self):
        ''' 手机号或发布会id错误 '''
        response = self.client.post('/sign_index_action/2/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"event id or phone error.", response.content)

    def test_sign_index_action_user_sign_has(self):
        ''' 用户已签到 '''
        response = self.client.post('/sign_index_action/2/', {"phone": "18611001101"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user has sign in.", response.content)

    def test_sign_index_action_sign_success(self):
        ''' 签到成功 '''
        response = self.client.post('/sign_index_action/1/', {"phone": "18611001100"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"sign in success!", response.content)
