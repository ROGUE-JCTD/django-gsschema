# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('gsschema.views',
    url(r'^$', 'index', name='index'),
    url(r'(?P<layer>\w+)/download', 'download', name='download'),
    url(r'(?P<layer>\w+)/describe', 'describe', name='describe'),
    url(r'(?P<layer>\w+)/upload', 'upload', name='upload'),
)
