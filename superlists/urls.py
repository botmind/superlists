from django.conf.urls import include, url
from lists import views as quote_views
from lists import urls as quote_urls

urlpatterns = [
	url(r'^$', quote_views.home_page, name='home'),
	url(r'^quotes/', include(quote_urls)),
    #url(r'^admin/', include(admin.site.urls)),
]
