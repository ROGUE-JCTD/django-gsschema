# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('gsschema_prj.gsschema.views',
    url(r'^index/$', 'index', name='index'),
)
