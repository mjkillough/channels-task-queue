#!/usr/bin/env python
# encoding: utf-8

import logging

from django.http import JsonResponse, Http404

import taskqueue
import taskqueue.models

from . import tasks


def start_dummy_task(request):
    # TODO: Should really @require_POST as this view has side-effects. However,
    #       to make it easier to test via the browser, we'll leave it off.
    task_context = tasks.dummy_sleeping_task.call_async(30)
    return JsonResponse(dict(success=True, task=task_context.as_dict))


def cancel_task(request, id):
    id = int(id)
    try:
        task_context = taskqueue.backends.backend.context_for_task_id(id)
    except taskqueue.models.TaskContext.DoesNotExist:
        raise Http404
    task_context.cancel()
    return JsonResponse(dict(success=True))


def task_info(request, id):
    id = int(id)
    try:
        task_context = taskqueue.backends.backend.context_for_task_id(id)
    except taskqueue.models.TaskContext.DoesNotExist:
        raise Http404
    return JsonResponse(dict(success=True, task=task_context.as_dict))
