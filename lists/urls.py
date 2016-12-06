from django.conf.urls import include, url
from django.contrib import admin
from lists import views

urlpatterns = [
	url(r'^new$', views.new_quote, name='new_quote'),
	url(r'^(\d+)/$', views.view_quote, name='view_quote'), #(\d+) captures any digits passed between /.../ and assigns it to an extra param passed to the view function (which we named author_id in views.py)
    #url(r'^admin/', include(admin.site.urls)),
]
