from django.conf.urls import url, include
from django.urls import path
from backend import views
# import views
urlpatterns = [
	path('login', views.login), 
	path('register', views.register),
	path('statecheck', views.statecheck),
	path('itve/getun/', views.interviewee_get_unfinished),
	path('itvr/getall/', views.interviewer_getall),
	path('room/getun/', views.room_get_unfinished),
	path('room/info/<int:roomid>/', views.room_getinfo),
	path('room/add/', views.room_add),
]
