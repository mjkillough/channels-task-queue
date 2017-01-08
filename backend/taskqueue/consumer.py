#!/usr/bin/env python
# encoding: utf-8

import json
import logging

import django.db.transaction

from . import exceptions

logger = logging.getLogger(__name__)


def run_task_consumer(msg):
    logger.info('Received task: (%i, %s, %r)',
        msg['id'], msg['name'], msg['parameters']
    )

    # Late import because Django's apps are a bit silly.
    from . import backends

    task_context = backends.backend.context_for_task_id(msg['id'])
    task = backends.backend.get_task_by_name(msg['name'])

    # Before calling the task synchronously, set its status to Running.
    with django.db.transaction.atomic():
        task_context.status = task_context.TaskStatus.Running
        task_context.save()

    try:
        ret = task.func(task_context, *msg['parameters'])
    except exceptions.CanceledError:
        logger.info('Cancelation while running task %i (%s)', msg['id'], msg['name'])
        with django.db.transaction.atomic():
            task_context.status = task_context.TaskStatus.Canceled
            task_context.save()
            return
    except Exception:
        logger.exception('Exception while running task %i (%s):', msg['id'], msg['name'])
        with django.db.transaction.atomic():
            task_context.status = task_context.TaskStatus.Failed
            task_context.save()
            return

    # Transition to Complete state and remember the return value.
    with django.db.transaction.atomic():
        task_context.status = task_context.TaskStatus.Complete
        task_context.return_json = json.dumps(ret)
        task_context.progress = 100
        task_context.save()

    logger.info('Task %i (%s) complete.', msg['id'], msg['name'])
    logger.debug('Task %i (%s) returned: %r', msg['id'], msg['name'], ret)
