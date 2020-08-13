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
	itves = Interviewee.objects.filter(status=0).values('name', 'mobile', 'email')
	return JsonResponse(list(itves), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['GET'])
def interviewer_getall(request):
	"""
	返回所有面试官和他们在不同时间段是否空闲。

	用法：GET /api/itvr/getall/
	- 返回：[{ 'name': str, 'mobile': str, 'email': str, free1: bool, free2: bool, free3: bool }, ...]
	"""
	itvrs = Interviewer.objects.values(
		'name', 'mobile', 'email', 'free1', 'free2', 'free3')
	return JsonResponse(list(itvrs), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['GET'])
def room_get_unfinished(request):
	"""
	返回所有未确定结果的面试

	用法：GET /api/room/getun/
	- 返回：[{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester__email': 面试官邮箱, 'interviewee__email': 候选人邮箱 }, ...]
	"""
	rooms = Room.objects.filter(interviewee__status=0)
	return JsonResponse(list(rooms.values('roomid', 'time', 'tester__email', 'interviewee__email')), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['GET'])
def room_getinfo(request, roomid):
	"""
	返回对应面试房间的面试时间、面试者等信息

	用法：GET /api/room/info/<int:roomid>/
	- 返回：
		- 成功：{ 'roomid': 6位数字（str）, 'time': 时间（0-2）, 'tester': 面试官邮箱, 'interviewee': 候选人邮箱, 'interviewer__name': 面试官名字, 'interviewee__name': 候选人名字 }
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

	return JsonResponse(j, json_dumps_params={'ensure_ascii': False})


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
		itvr = Interviewer.objects.get(pk=r)
		r = Room.objects.create(roomid=rid, time=t, tester=itvr,
		                        interviewee=Interviewee.objects.get(pk=e))
		if t == 0:
			itvr.free1 = False
		elif t == 1:
			itvr.free2 = False
		else:
			itvr.free3 = False

		itvr.save()
		r.save()
	except Exception as e:
		roomid = ''
	else:
		roomid = str(rid)

	return JsonResponse({'roomid': roomid})


@api_view(['POST'])
def room_delete(request):
	"""
	删除面试。

	用法：POST /api/room/delete/
	- 请求内容：`{ 'roomid': int }`
	- 返回内容：`{ 'success': bool }`
	"""
	rid = request.data.get('roomid')

	success = True
	try:
		Room.objects.get(pk=rid).delete()
	except:
		success = False

	return JsonResponse({'success': success})


@api_view(['POST'])
def room_rate(request):
	"""
	给面试打分。

	用法：POST /api/room/rate/
	- 请求内容：`{ 'roomid': int, 'score': int (0-100), 'remark': 评语（str）}`
	- 返回内容：`{ 'success': bool }`
	"""
	d = request.data
	rid, score, remark = d.get('roomid'), d.get('score'), d.get('remark')

	success = True
	try:
		r = Room.objects.get(pk=rid)
		r.score, r.remark = score, remark
		r.save()
	except Exception as e:
		print(e)
		success = False

	return JsonResponse({'success': success})


@api_view(['GET'])
def room_review(request):
	"""
	返回面试结果（UI-ALL第28页）。

	用法：GET /api/room/review/
	- 返回内容：`[{ 'roomid': str, 'interviewee__name': 候选人姓名(str), 'interviewer__name': 面试官姓名(str), 'score': int(0-100), 'time': int(0-2), 'interviewee__status': int(0-2) }, ...]
	- status：0代表未分配，1代表拒绝，2代表录用
	"""
	res = Room.objects.values('roomid', 'interviewee__name',
	                          'tester__name', 'score', 'time', 'interviewee__status')
	return JsonResponse(list(res), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def room_get_remark(request):
	"""
	返回面试评语

	用法：POST /api/room/remark/
	- 请求内容：`{ 'roomid': int }`
	- 返回内容：`{ 'remark': str }`
	"""
	res = Room.objects.get(pk=request.data.get('roomid')).remark
	return JsonResponse({'remark': res}, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def room_decide(request):
	"""
	确定是否录用，支持批量修改

	用法：POST /api/room/decide/
	- 请求内容：`{ 'rooms': [int, int, ...], 'status': int(0-2) }`
	- 返回内容：`{ 'success': bool }`
	"""
	rs, status = request.data.get('rooms'), request.data.get('status')

	success = True
	try:
		ives = Room.objects.filter(pk__in=rs).values_list('interviewee', flat=True)
		Interviewee.objects.filter(pk__in=ives).update(status=status)
	except Exception as e:
		print(e)
		success = False

	return JsonResponse({'success': success})


@api_view(['GET'])
def itve_getall(request):
	"""
	返回所有候选人。

	用法：GET /api/itve/getall/
	返回：`[{ 'name': str, 'mobile': str, 'email': str, 'status': int }, ...]`
	"""
	itves = Interviewee.objects.values()
	return JsonResponse(list(itves), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['GET'])
def hr_getall(request):
	"""
	返回所有HR

	用法：GET /api/itve/getall/
	返回：`[{ 'name': str, 'mobile': str, 'email': str }, ...]`
	"""
	hrs = Hr.objects.values('name', 'mobile', 'email')
	return JsonResponse(list(hrs), safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def itve_set(request):
	"""
	修改候选人的信息，若`old_email`域为空字符串，则新建一个候选人。

	用法：POST /api/itve/
	- 请求内容：`{ 'name': str, 'mobile': str, 'old_email': str, 'new_email': str }`
	- 返回：`{ 'success': bool }`
	"""
	d = request.data
	n, m, oe, ne = d.get('name'), d.get(
		'mobile'), d.get('old_email'), d.get('new_email')

	success = True
	try:
		if oe:
			itve = Interviewee.objects.get(pk=oe)
			itve.name, itve.mobile = n, m
			if itve.email != ne:
				itve.email = ne
				Interviewee.objects.get(pk=oe).delete()
			itve.save()
		else:
			Interviewee.objects.create(name=n, mobile=m, email=ne)
	except:
		success = False

	return JsonResponse({'success': success})


@api_view(['POST'])
def hr_set(request):
	"""
	修改HR的信息，若`old_email`域为空字符串，则新建一个HR。

	用法：POST /api/itve/
	- 请求内容：`{ 'name': str, 'mobile': str, 'password': str, 'old_email': str, 'new_email': str }`
	- 返回：`{ 'success': bool }`
	"""
	d = request.data
	n, m, pw, oe, ne = d.get('name'), d.get('mobile'), d.get(
		'password'), d.get('old_email'), d.get('new_email')

	success = True
	try:
		if oe:
			hr = Hr.objects.get(pk=oe)
			hr.name, hr.mobile, hr.password = n, m, pw
			if hr.email != ne:
				hr.email = ne
				Hr.objects.get(pk=oe).delete()
			hr.save()
		else:
			Hr.objects.create(name=n, mobile=m, password=pw, email=ne)
	except:
		success = False

	return JsonResponse({'success': success})


@api_view(['POST'])
def itvr_set(request):
	"""
	修改面试官的信息，若`old_email`域为空字符串，则新建一个面试官。

	用法：POST /api/itvr/
	- 请求内容：`{ 'name': str, 'mobile': str, 'password': str, 'old_email': str, 'new_email': str, 'free1': bool, 'free2': bool, 'free3': bool }`
	- 返回：`{ 'success': bool }`
	"""
	d = request.data
	n, m, pw, oe, ne = d.get('name'), d.get('mobile'), d.get(
		'password'), d.get('old_email'), d.get('new_email')
	f1, f2, f3 = d.get('free1'), d.get('free2'), d.get('free3')

	success = True
	try:
		if oe:
			itvr = Interviewer.objects.get(pk=oe)
			itvr.name, itvr.mobile, itvr.password = n, m, pw
			itvr.free1, itvr.free2, itvr.free3 = f1, f2, f3
			if ne != itvr.email:
				itvr.email = ne
				Interviewer.objects.get(pk=oe).delete()
			itvr.save()
		else:
			Interviewer.objects.create(
				name=n, mobile=m, password=pw, email=ne, free1=f1, free2=f2, free3=f3)
	except:
		success = False

	return JsonResponse({'success': success})
