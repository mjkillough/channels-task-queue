#!/usr/bin/env python
# encoding: utf-8

import enum

from django.db import models
import django.db.transaction

from . import exceptions


def _enum_as_choices(enum):
    """Return an enum.Enum as a Django 'choices' tuple."""
    return (
        (member.name, member.value)
        for member in enum
    )


class TaskContext(models.Model):

    TaskStatus = enum.IntEnum('TaskStatus', [
        'Queued',
        'Running',
        'Canceled',
        'Failed',
        'Complete',
    ])
    status = models.IntegerField(choices=_enum_as_choices(TaskStatus))

    # JSON dictionary containing parameters passed into the task. Certain
    # backends (such as the Channels backend) may choose to send these to the
    # task by some other means. Stored on the model so that all information
    # about the task is available after it has completed.
    parameters_json = models.TextField()

    # Task progress, stored as integer 0-100, unfortunately not a DB constraint.
    progress = models.IntegerField(default=0)

    # Those outside the task can set this to signal to the task that it should
    # terminate early. (This field being set does not mean the task has been
    # terminated - see `status`).
    cancel_signal = models.BooleanField(default=False)

    # JSON serialized value (possibly null) returned by the task.
    result_json = models.TextField(default='null')

    def refresh(self):
        """Gets the latest state for the task"""
        # Simple encapsulation around Django's model function.
        return self.refresh_from_db()

    def cancel(self):
        with django.db.transaction.atomic():
            self.cancel_signal = True
            self.save()

    def throw_if_canceled(self):
        """Raises `CanceledError` exception if the task has been canceled.

        Expected to be called periodically from within tasks, which should allow
        the error to propogate to the consumer/task runner.
        """
        self.refresh()
        if self.cancel_signal:
            raise exceptions.CanceledError
