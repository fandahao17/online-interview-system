from django.conf.urls import url, include
from django.urls import path
from backend import views
# import views
urlpatterns = [
	path('login', views.login), 
	path('register', views.register),
	path('statecheck', views.statecheck)
]
