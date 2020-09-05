from django.test import TestCase
from django.test import Client
from .models import Interviewee

# Create your tests here.
class TestInterviewee(TestCase):
    '''
    测试功能：
    itve_set --修改、创建候选人信息
    interviewee_get_unfinished --候选人是否被录用
    itve_getall --返回所有候选人
    itve_delete --删除候选人

    class Interviewee(models.Model):
    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, default='11111111111')
    email = models.EmailField(primary_key=True)
    status = models.IntegerField(default=0)
    '''

    @classmethod
    def setUpTestData(cls):
        #创建三条候选人信息
        Interviewee.objects.create(name='A', email='a@mail.ustc.edu.cn')
        Interviewee.objects.create(name='B', email='b@mail.ustc.edu.cn', status=1)
        Interviewee.objects.create(name='C', email='c@ustc.edu.cn')
    
    def setUp(self):
        Interviewee.refresh_from_db()
    
    def test_itve_getun(self):
        c = Client()
        response = c.get('/itve/getun')
        self.assertEqual(len(response.json()['email']), 1)

    def test_getall(self):
        c = Client()
        response = c.get('/itve/getall')
        self.assertEqual(len(response.json()['email']), 3)

    def test_intve_set(self):
        c = Client()
        # test update interviewee
        response = c.post('/itve/', {'name': 'D', 'mobile': '12222222222', 'old_email': 'a@mail.ustc.edu.cn', 'new_email': 'd@mail.ustc.edu.cn'})
        self.assertEqual(response.json()['success'], True)
        response = Interviewee.objects.get(email='d@mail.ustc.edu.cn')
        self.assertEqual(response.name, 'D')
        #test create interviewee
        response = c.post('/itve/', {'name': 'N', 'mobile': '13222222222', 'new_email': '122@mail.ustc.edu.cn'})
        self.assertEqual(response.json()['success'], True)
        response = Interviewee.objects.get(email='122@mail.ustc.edu.cn')
        self.assertEqual(response.mobile, '13222222222')

    def test_itve_delete(self):
        c = Client()
        response = c.delete('/itve/delete', {'name': 'C', 'email': 'c@mail.ustc.edu.cn'})
        self.assertEqual(response.json()['success'], True)  
