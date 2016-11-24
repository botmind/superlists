from django.conf.urls import include, url
from django.contrib import admin
from lists import views

urlpatterns = [
	url(r'^$', views.home_page, name='home'),
	url(r'^quotes/new$', views.new_quote, name='new_quote'),
	url(r'^quotes/(\d+)/$', views.view_quote, name='view_quote'), #(\d+) captures any digits passed between /.../ and assigns it to an extra param passed to the view function (which we named author_id in views.py)
    url(r'^quotes/(\d+)/add_quote$', views.add_quote, name='add_quote')
    #url(r'^admin/', include(admin.site.urls)),
]
