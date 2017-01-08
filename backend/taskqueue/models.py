#!/usr/bin/env python
# encoding: utf-8

import enum

from django.db import models


def _enum_as_choices(enum):
    """Return an enum.Enum as a Django 'choices' tuple."""
    return (
        (member.name, member.value)
        for member in enum
    )


class TaskContext(models.Model):

    TaskStatus = enum.Enum('TaskStatus', [
        'Queued',
        'Running',
        'Canceled',
        'Complete',
    ])
    status = models.IntegerField(choices=_enum_as_choices(TaskStatus))

    # JSON dictionary containing parameters passed into the task. Certain
    # backends (such as the Channels backend) may choose to send these to the
    # task by some other means. Stored on the model so that all information
    # about the task is available after it has completed.
    parameters_json = models.TextField()

    # Task progress, stored as integer 0-100, unfortunately not a DB constraint.
    progress = models.IntegerField()

    # Those outside the task can set this to signal to the task that it should
    # terminate early. (This field being set does not mean the task has been
    # terminated - see `status`).
    cancel_signal = models.BooleanField()

    # JSON serialized value (possibly null) returned by the task.
    result_json = models.TextField()

    def refresh(self):
        """Gets the latest state for the task"""
        # Simple encapsulation around Django's model function.
        return self.refresh_from_db()
