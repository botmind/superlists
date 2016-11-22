from django.conf.urls import include, url
from django.contrib import admin
from lists import views

urlpatterns = [
	url(r'^$', views.home_page, name='home'),
	url(r'^quotes/new$', views.new_quote, name='new_quote'),
	url(r'^quotes/quote-list/$', views.view_quote, name='view_quote')
    #url(r'^admin/', include(admin.site.urls)),
]
