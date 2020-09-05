from django.test import TestCase
from django.test import Client
from ..models import Interviewer, Interviewee, Room
import json

class TestInterviewer(TestCase):
    '''
    测试功能：
    itvr_set --修改、新建面试官信息
	itvr_set_time --修改面试官的空闲时间
	interviewer_getall --返回面试官和他们在不同时间是否空闲
	itvr_get_itves --返回和面试官相关的候选人信息
	itvr_delete --列表中所有面试官删除

    name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=20, default='11111111111')
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128, default='123456')
    free1 = models.BooleanField(default=True)
    free2 = models.BooleanField(default=True)
    free3 = models.BooleanField(default=True)

    roomid = models.IntegerField(primary_key=True)
    time = models.IntegerField()
    score = models.IntegerField(null=True, blank=True)
    remark = models.CharField(max_length=500, null=True, blank=True)
    tester = models.ForeignKey('Interviewer', on_delete=models.CASCADE)
    interviewee = models.ForeignKey('Interviewee', on_delete=models.CASCADE, null=True)
    '''
    @classmethod
    def setUpTestData(cls):
        Interviewer.objects.create(name='aa', email='aa@ustc.edu.cn', free1=False)
        Interviewer.objects.create(name='bb', email='bb@ustc.edu.cn', free2=False)
        Interviewer.objects.create(name='cc', email='cc@ustc.edu.cn', free3=False)
        Interviewee.objects.create(name='A', email='A@mail.ustc.edu.cn')
        
    def test_itvr_set(self):
        c = Client()
        response = c.post('/itvr/', {'name':'dd', 'mobile': '12345674567', 'new_email': 'dd@ustc.edu.cn','free1':True, 'free2': False, 'free3': False})
        self.assertEqual(json.loads(response.content.decode('utf8'))['success'], True)
        response = c.post('/itvr/', {'name':'aa', 'mobile':'17300000000', 'old_email': 'aa@ustc.edu.cn','free1':True, 'free2':False, 'free3': False})
        self.assertEqual(json.loads(response.content.decode('utf8'))['success'], True)
    
    def test_itvr_set_time(self):
        c = Client()
        response = c.post('/itvr/setfreetime/', {'email': 'bb@ustc.edu.cn', 'free1': False, 'free2': True, 'free3': True})
        self.assertEqual(json.loads(response.content.decode('utf8'))['success'], True)

    def test_itvr_getall(self):
        c = Client()
        response = c.get('/itvr/getall/')
        self.assertEqual(len(json.loads(response.content.decode('utf8'))), 3)
    
    def test_itvr_delete(self):
        c = Client()
        response = c.delete('/itvr/delete/')
        self.assertEqual(json.loads(response.content.decode('utf8'))['success'], True)
       
    def test_itvr_get_itve(self):
        '''
        roomid = models.IntegerField(primary_key=True)
        time = models.IntegerField()
        score = models.IntegerField(null=True, blank=True)
        remark = models.CharField(max_length=500, null=True, blank=True)
        tester = models.ForeignKey('Interviewer', on_delete=models.CASCADE)
        interviewee = models.ForeignKey('Interviewee', on_delete=models.CASCADE, null=True)
        '''
        Itve = Interviewee.objects.get(pk='A@mail.ustc.edu.cn')
        Itvr = Interviewer.objects.get(pk='aa@ustc.edu.cn')
        Room.objects.create(roomid=1, time=1, tester=Itvr, interviewee=Itve)
        c = Client()
        response = c.get('/itvr/getitves/aa@ustc.edu.cn/')
        print(response)
        self.assertEqual(len(json.loads(response.content.decode('utf8'))), 1)
        
