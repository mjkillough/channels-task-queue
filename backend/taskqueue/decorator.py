#!/usr/bin/env python
# encoding: utf-8

from . import backends


class Task:

    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        backends.backend.register_task(self)

    def call_async(self, *args):
        """Calls the wrapped Task asynchronously."""
        # TODO: Check the arity of args matches the function, where we can?
        id = backends.backend.push_task(self, args)
        return backends.backend.context_for_task_id(id)


def task():
    """Wraps a function, turning it into a task.

    The function should take a `TaskContext` as its first argument, followed by
    an optional list of positional arguments. The function can return a result.

    The wrapped function is presented as a `Task`, whose `.call_async(*args)`
    method should be used to call the task async.
    """
    def decorator(func):
        return Task(func)
    return decorator
