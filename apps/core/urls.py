from django.urls import path
from django.contrib.auth import views
from django.contrib.auth import views as auth_views #import this
from . import views

urlpatterns = [
	path('',views.login_view, name='home'),
	path('logout/',auth_views.LogoutView.as_view(), name='logout'),
	# shared link
	

	
	
	]

