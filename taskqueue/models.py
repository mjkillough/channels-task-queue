#!/usr/bin/env python
# encoding: utf-8

import enum
import json

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

    @property
    def as_dict(self):
        return dict(
            id=self.id,
            status=self.status,
            status_string=self.TaskStatus(self.status).name, # XXX: I18N
            parameters=json.loads(self.parameters_json),
            progress=self.progress,
            result=json.loads(self.result_json),
            canceling=self.cancel_signal and self.status != self.TaskStatus.Canceled,
        )

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

    def set_progress(self, value):
        assert 0 <= value <= 100
        with django.db.transaction.atomic():
            self.progress = value
            self.save()
