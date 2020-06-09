from django.shortcuts import render, HttpResponse
import time
from rest_framework.authtoken.models import Token
from backend import models
from django.http import JsonResponse
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def login(request):
	ret = {"code": 1000, "msg": "Begin msg", "type": "-1", "token": ""}
	try:
		name = request.data.get('name')
		password = request.data.get('password')
		identity = request.data.get('identity')
		if identity == 1:
			obj = models.Interviewer.objects.filter(name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)

			token = str(time.time()) + name
			models.interToken.objects.update_or_create(name=obj, defaults={'token': token})
			ret["msg"] = "Login success"
			ret["type"] = "1"
			ret["token"] = token
			return JsonResponse(ret)

		elif identity == 2:
			obj = models.Super.objects.filter(name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)

			token = str(time.time()) + name
			models.superToken.objects.update_or_create(name=obj, defaults={'token': token})
			ret["msg"] = "Login success"
			ret["type"] = "2"
			ret["token"] = token
			return JsonResponse(ret)

		elif identity == 3:
			obj = models.Hr.objects.filter(name=name, password=password).first()
			if not obj:
				ret["code"] = '1001'
				ret["msg"] = 'Name or password or identity error'
				return JsonResponse(ret)
			token = str(time.time()) + name
			models.hrToken.objects.update_or_create(name=obj, defaults={'token': token})
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
			obj = models.Interviewer.objects.filter(name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = models.Interviewer(name=name, mobile=mobile, email=email, password=password)
			b.save()
		elif identity == 2:
			obj = models.Super.objects.filter(name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = models.Super(name=name, mobile=mobile, email=email, password=password)
			b.save()
		elif identity == 3:
			obj = models.Hr.objects.filter(name=name, mobile=mobile, email=email, password=password)
			if obj:
				ret["code"] = 1003
				ret["msg"] = 'Repeat registration, change your please change the registration information or log in'
				return JsonResponse(ret)
			b = models.Hr(name=name, mobile=mobile, email=email, password=password)
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
			obj = models.Interviewer.objects.filter(name=name).first() # 获取token对应的obj
			real_token = obj.interToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else :
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

		elif identity == 2:
			obj = models.Super.objects.filter(name=name).first() # 获取token对应的obj
			real_token = obj.superToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else :
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

		elif identity == 3:
			obj = models.Hr.objects.filter(name=name).first() # 获取token对应的obj
			real_token = obj.hrToken.token
			if token == real_token:
				ret["code"] = 1000
				ret["msg"] = "Successful verification"
			else :
				ret["code"] = 1001
				ret["msg"] = "Verification failed"

	except Exception as e:
		ret["code"] = 1002
		ret["msg"] = 'Exception error, please try again'

		
