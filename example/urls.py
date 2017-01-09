#!/usr/bin/env python
# encoding: utf-8

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^start/$', views.start_dummy_task),
    url(r'^cancel/([0-9]+)/$', views.cancel_task),
    url(r'^task/([0-9]+)/$', views.task_info),
]
