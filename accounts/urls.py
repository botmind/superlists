from django.conf.urls import url
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
]
