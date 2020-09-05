from django.test import TestCase, Client
from ..models import *
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class HrViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Hr.objects.create(name='cbn', mobile='11111111111', email='940107412@qq.com', password='123456')
    Hr.objects.create(name='lsq', mobile='11111111111', email='940107410@qq.com', password='123456')
    Hr.objects.create(name='lcy', mobile='11111111111', email='940107411@qq.com', password='123456')

  def test_hr_set(self):
    """
    Test hr set
    """
    url = '/hr/'
    data = {'name': 'cbn', 'mobile': '11111111111', 'password': 123456, 'old_email': '940107412@qq.com', 'new_email': '944107412@qq.com'}
    client = Client()
    response = client.post(url, data)
    json_data = json.loads(response.content.decode('utf8'))
    self.assertEqual(json_data['success'], True)


  def test_hr_all(self):
    url = '/hr/getall/'
    data = {''}
    client = Client()
    response = client.get(url)
    json_data = json.loads(response.content.decode('utf8')) 
    length = len(json_data)
    self.assertEqual(length, 3)
