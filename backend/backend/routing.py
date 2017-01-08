#!/usr/bin/env python

from channels.routing import route

import taskqueue


channel_routing = [
    route('taskqueue.queue', taskqueue.run_task_consumer),
]
