from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.image_list, name='image_list'),
	url(r'^id/(?P<id>[0-9]+)', views.image_page, name='image_page'),
	url(r'^add', views.image_add, name='image_add'),
	url(r'^delete/(?P<id>[0-9]+)', views.image_delete, name='image_delete'),
]
