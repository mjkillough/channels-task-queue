#!/usr/bin/env python
# encoding: utf-8

import math
import time

import taskqueue


@taskqueue.task()
def dummy_sleeping_task(task, total_time_in_seconds):
    sleep_period = 2 # seconds
    total_sleep_ticks = math.ceil(total_time_in_seconds / sleep_period)
    for tick in range(total_sleep_ticks):
        progress = (tick / total_sleep_ticks) * 100
        task.set_progress(progress)
        print('Tick %i: %i' % (task.id, progress))
        time.sleep(sleep_period)
