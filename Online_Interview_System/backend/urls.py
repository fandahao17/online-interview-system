from django.conf.urls import url, include
from django.urls import path
from backend import views
# import views
urlpatterns = [
	path('login', views.login), 
	path('register', views.register),
	path('statecheck', views.statecheck),
	path('itve/', views.itve_set),
	path('itve/getun/', views.interviewee_get_unfinished),
	path('itve/getall/', views.itve_getall),
	path('itve/delete/', views.itve_delete),
	path('itvr/', views.itvr_set),
	path('itvr/getall/', views.interviewer_getall),
	path('itvr/delete/', views.itvr_delete),
	path('hr/', views.hr_set),
	path('hr/getall/', views.hr_getall),
	path('hr/delete/', views.hr_delete),
	path('room/getun/', views.room_get_unfinished),
	path('room/info/<int:roomid>/', views.room_getinfo),
	path('room/video/<int:roomid>/', views.room_storevideo),
	path('room/add/', views.room_add),
	path('room/delete/', views.room_delete),
	path('room/rate/', views.room_rate),
	path('room/review/', views.room_review),
	path('room/remark/', views.room_get_remark),
	path('room/decide/', views.room_decide),
	path('problem/<int:pid>/', views.problem_get),
	path('problem/getall/', views.problem_getall),
]
