#!/usr/bin/env python
# encoding: utf-8

from django.http import JsonResponse

from . import tasks


def initiate_dummy_task(request):
    # TODO: Should really @require_POST as this view has side-effects. However,
    #       to make it easier to test via the browser, we'll leave it off.
    tasks.dummy_sleeping_task.call_async(30)
    return JsonResponse(dict(success=True))
