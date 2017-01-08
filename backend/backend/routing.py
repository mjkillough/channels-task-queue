#!/usr/bin/env python

from channels.routing import route

from . import consumer


channel_routing = [
    route('taskqueue.queue', consumer.run_task_consumer),
]
