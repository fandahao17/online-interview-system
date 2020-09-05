from django.test import TestCase, Client
from ..models import *
from django.test.utils import setup_test_environment

# Create your tests here.
class ProblemTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Problem.objects.create(
            id = 1024,
            name = "最长公共前缀",
            description = "编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 \"\"。",
            input_desc = "所有输入只包含小写字母 a-z",
            output_desc = "字符串数组中的最长公共前缀",
            input_sample = "[\"flower\",\"flow\",\"flight\"]",
            output_sample = "fl"
        )
        Problem.objects.create(
            id = 1025,
            name = "两数之和",
            description = "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。\n你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。",
            input_sample = "nums = [2, 7, 11, 15], target = 9",
            output_sample = "[0, 1]"
        )

    def setUp(self):
        pass

    def test_problem_get(self):
        client = Client()
        response = client.get('/problem/1025/')
        json_data = eval(response.content.decode('utf8'))
        # self.assertEqual(json_data['id'], 1025)
        self.assertEqual(json_data['name'], "两数之和")
        self.assertEqual(json_data['desc'], "给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那两个整数，并返回他们的数组下标。\n你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。")
        self.assertEqual(json_data['input_sample'], "nums = [2, 7, 11, 15], target = 9")
        self.assertEqual(json_data['output_sample'], "[0, 1]")
        
        response = client.get('/problem/1024/')
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data['input'], "所有输入只包含小写字母 a-z")
        self.assertEqual(json_data['output'], "字符串数组中的最长公共前缀")

def test_problem_getall(self):
        client = Client()
        response = client.get('/problem/getall/')
        json_data = eval(response.content.decode('utf8'))
        self.assertEqual(json_data[0]['id'], 1024)
        self.assertEqual(json_data[1]['id'], 1025)
        self.assertEqual(json_data[1]['name'], "两数之和")
        self.assertEqual(json_data[0]['name'], "最长公共前缀")
