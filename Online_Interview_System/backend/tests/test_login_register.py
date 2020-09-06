from django.test import TestCase, Client
from ..models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class LoginRegisterViewtest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Interviewer.objects.create(name='cbn', mobile='11111111111', email='940107412@qq.com', password='123456', free1=True, free2=True, free3=True)
    Super.objects.create(name='cbn', mobile='11111111111', email='940107412@qq.com', password='123456')
    Hr.objects.create(name='cbn', mobile='11111111111', email='940107412@qq.com', password='123456')

  def test_login(self):
    url = '/login'
    client = Client()
    data = {'email': '940107412@qq.com', 'password': '123456', 'identity': int(3)}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    print("--login--")
    print(json_data)
    self.assertEqual(json_data['code'], 1000)

    data = {'email': '940107412@qq.com', 'password': '123456', 'identity': 2}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    self.assertEqual(json_data['code'], 1000)

    data = {'email': '940107412@qq.com', 'password': '123456', 'identity': 1, 'free1': True, 'free2': True, 'free3': True}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    print("Identity 1")
    self.assertEqual(json_data['code'], 1000)

  def test_register(self):
    url = '/register'
    client = Client()
    data = {'name': 'cbn2', 'password': '123456', 'mobile': '11111111111', 'email': '9401074123@qq.com', 'identity': 3}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    self.assertEqual(json_data['code'], 1000) 

    data = {'name': 'cbn2', 'password': '123456', 'mobile': '11111111111', 'email': '9401074124@qq.com', 'identity': 2}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    self.assertEqual(json_data['code'], 1000)  

    data = {'name': 'cbn', 'password': '123456', 'mobile': '11111111111', 'email': '9401074125@qq.com', 'identity': 1, 'free1': True, 'free2': True, 'free3': True}
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    print("Identity 1")
    self.assertEqual(json_data['code'], 1000) 
