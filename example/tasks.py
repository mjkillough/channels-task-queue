#!/usr/bin/env python
# encoding: utf-8

import math
import time

import taskqueue


@taskqueue.task()
def dummy_sleeping_task(task, total_time_in_seconds):
    sleep_period = 0.1 # seconds
    total_sleep_ticks = math.ceil(total_time_in_seconds / sleep_period)
    for tick in range(total_sleep_ticks):
        # Check if we've been canceled. Will raise an exception if we have,
        # which the task runner will catch and handle.
        task.throw_if_canceled()

        progress = (tick / total_sleep_ticks) * 100
        task.set_progress(progress)
        print('Tick %i: %i' % (task.id, progress))

        time.sleep(sleep_period)
