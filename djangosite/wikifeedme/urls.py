from django.conf.urls import patterns, url

from wikifeedme import views

urlpatterns = patterns('',
                       url(r'^$', views.index),
                       url(r'^feedMe/$', views.feedMe),
                       url(r'^about/$', views.about),
)
