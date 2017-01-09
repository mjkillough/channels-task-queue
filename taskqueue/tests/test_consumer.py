#!/usr/bin/env python
# encoding: utf-8

import json
import unittest

import django.test

from .. import backends, consumer, models


class ConsumerTests(django.test.TestCase):
    pass

    # TODO: I've run out of time today. :) I would like tests to check:

    # - The task status transitions to Running at the time the task is called.
    # - The task correctly handles being canceled, including setting the status.
    # - The task correctly updated to 'Failed' if an exception is thrown in the task func.
    # - The task transitions to 'Complete' when the task func finished.
    # - The value returned from the task func is serialized as JSON on the TaskContext.
    # - The task always has a progress of 100 when it completes.
