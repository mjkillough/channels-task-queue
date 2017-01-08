#!/usr/bin/env python
# encoding: utf-8

import math
import time

import taskqueue


@taskqueue.task()
def dummy_sleeping_task(total_time_in_seconds):
    sleep_period = 2 # seconds
    total_sleep_ticks = math.ceil(total_time_in_seconds / sleep_period)
    for tick in range(total_sleep_ticks):
        print('tick')
        time.sleep(sleep_period)
