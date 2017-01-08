#!/usr/bin/env python
# encoding: utf-8

from django.http import JsonResponse

from . import tasks


def initiate_dummy_task(request):
    tasks.dummy_task.call_async()
    return JsonResponse(dict(success=True))
