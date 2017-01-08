#!/usr/bin/env python
# encoding: utf-8

import taskqueue


@taskqueue.task()
def dummy_task(self):
    pass
