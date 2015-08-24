from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^logout$', views.logout_view, name='logout_view'),
	url(r'^$', views.image_list, name='image_list'),
	url(r'^id/(?P<id>[0-9]+)', views.image_page, name='image_page'),
	url(r'^add', views.image_add, name='image_add'),
	url(r'^delete/(?P<id>[0-9]+)', views.image_delete, name='image_delete'),
	url(r'^api/$', views.api_list, name='api_list'),
	url(r'^api/add/$', views.api_add, name='api_add'),
	url(r'^api/id/(?P<id>[0-9]+)$', views.api_details, name='api_details'),
	url(r'^api/delete/(?P<id>[0-9]+)$', views.api_delete, name='api_delete'),
]
