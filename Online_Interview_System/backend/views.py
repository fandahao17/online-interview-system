from django.shortcuts import render, HttpResponse
from django.core import serializers
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from .models import *
import time
import json
import random
# Create your views here.


@api_view(['POST'])
def login(request):
	ret = {"code": 1000, "msg": "Begin msg", "type": "-1", "token": ""}
	try:
		name = request.data.get('name')
		password = request.data.get('password')
		identity = request.data.get('identity')
		if identity == 1:
			obj = Interviewer.objects.filter(
				name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)

			token = str(time.time()) + name
			interToken.objects.update_or_create(
				name=obj, defaults={'token': token})
			ret["msg"] = "Login success"
			ret["type"] = "1"
			ret["token"] = token
			return JsonResponse(ret)

		elif identity == 2:
			obj = Super.objects.filter(name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)

			token = str(time.time()) + name
			superToken.objects.update_or_create(
				name=obj, defaults={'token': token})
			ret["msg"] = "Login success"
			ret["type"] = "2"
			ret["token"] = token
			return JsonResponse(ret)

		elif identity == 3:
			obj = Hr.objects.filter(name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)
			token = str(time.time()) + name
			hrToken.objects.update_or_create(name=obj, defaults={'token': token})
			ret["msg"] = "Login success"
			ret["type"] = "3"
			ret["token"] = token
			return JsonResponse(ret)
		else:
			ret["code"] = 1003
			ret["msg"] = "Search Error"
			return JsonResponse(ret)

	except Exception as e:
		print(e)
		ret["code"] = 1002
		ret["msg"] = 'Request Error'
	return JsonResponse(ret)


@api_view(['POST'])
def register(request):
	ret = {"code": 1000, "msg": 'Begin msg', "type": "-1"}
	try:
		name = request.data.get('name')
		password = request.data.get('password')
		mobile = request.data.get('mobile')
		email = request.data.get('email')
		identity = request.data.get('identity')
		if identity == 1:
			obj = Interviewer.objects.filter(
				name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = Interviewer(name=name, mobile=mobile,
			                       email=email, password=password)
			b.save()
		elif identity == 2:
			obj = Super.objects.filter(
				name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = Super(name=name, mobile=mobile, email=email, password=password)
			b.save()
		elif identity == 3:
			obj = Hr.objects.filter(
				name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = Hr(name=name, mobile=mobile, email=email, password=password)
			b.save()
		else:
			ret["code"] = 1001
			ret["msg"] = 'Search error'
			return JsonResponse(ret)

		ret["code"] = 1000
		ret["msg"] = 'Register success'
		ret["type"] = str(identity)
		return JsonResponse(ret)
	except Exception as e:
		ret["code"] = 1002
		ret["msg"] = 'Exception error, please try again'
		return JsonResponse(ret)


@api_view(['POST'])
def statecheck(request):
	ret = {"code": 1000, "msg": "Error"}
	try:
		name = request.data.get('name')
		token = request.data.get('token')
		identity = request.data.get('identity')
		if identity == 1:
			obj = Interviewer.objects.filter(name=name).first()  # 获取token对应的obj
			real_token = obj.interToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else:
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

		elif identity == 2:
			obj = Super.objects.filter(name=name).first()  # 获取token对应的obj
			real_token = obj.superToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else:
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

		elif identity == 3:
			obj = Hr.objects.filter(name=name).first()  # 获取token对应的obj
			real_token = obj.hrToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else:
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

	except Exception:
		ret["code"] = 1002
		ret["msg"] = 'Exception error, please try again'


@api_view(['GET'])
def interviewee_get_unfinished(request):
	"""
	返回所有尚未确定是否录用的候选人，HR可以给这些候选人安排面试。

	用法：GET /api/itve/getun/
	- 返回：[{ 'name': str, 'mobile': str, 'email': str }, ...]
	"""
	itves = Interviewee.objects.filter(accept__isnull=True).defer('accept')
	return JsonResponse(json.dumps(list(itves.values())), safe=False)


@api_view(['GET'])
def interviewer_getall(request):
	"""
	返回所有面试官和他们在不同时间段是否空闲。

	用法：GET /api/itvr/getall/
	- 返回：[{ 'name': str, 'mobile': str, 'email': str, free1: bool, free2: bool, free3: bool }, ...]
	"""
	itvrs = Interviewer.objects.defer('password').values()
	return JsonResponse(json.dumps(list(itvrs)), safe=False)


@api_view(['GET'])
def room_get_unfinished(request):
	"""
	返回所有未确定结果的面试

	用法：GET /api/room/getun/
	- 返回：[{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱 }, ...]
	"""
	rooms = Room.objects.filter(interviewee__accept__isnull=True).only(
		'roomid', 'time', 'tester', 'interviewee')
	return JsonResponse(json.dumps(list(rooms.values())), safe=False)


@api_view(['GET'])
def room_getinfo(request, roomid):
	"""
	返回对应面试房间的面试时间、面试者等信息

	用法：GET /api/room/info/<int:roomid>/
	- 返回：
		- 成功：{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱, 'rname': 面试官名字, 'ename': 候选人名字 }
		- 失败：{ 'roomid': 空字符串 }
	"""
	try:
		r = Room.objects.get(pk=roomid)
	except Exception as e:
		print(e)
		return JsonResponse({'roomid': ''})
	else:
		j = {'roomid': r.roomid, 'time': r.time,
				'tester': r.tester.email, 'interviewee': r.interviewee.email}
		j['rname'] = r.tester.name
		j['ename'] = r.interviewee.name

	return JsonResponse(j)


@api_view(['POST'])
def room_add(request):
	"""
	新建一个面试

	用法：POST /api/room/add/
	- 请求内容：{ 'itve': 候选人邮箱(str), 'itvr': 面试官邮箱(str), 'time': 面试时间，范围0-2(int) }
	- 返回内容：{ 'roomid': 6位数字房间号(str)，若失败则返回空 }
	"""
	rid = random.randint(100000, 999999)
	while Room.objects.filter(pk=rid).exists():
		rid = random.randint(100000, 999999)

	d = request.data
	t, e, r = d.get('time'), d.get('itve'), d.get('itvr')
	try:
		r = Room.objects.create(roomid=rid, time=t, tester=Interviewer.objects.get(
			pk=r), interviewee=Interviewee.objects.get(pk=e))
		r.save()
	except Exception as e:
		roomid = ''
	else:
		roomid = str(rid)

	return JsonResponse({'roomid': roomid})
