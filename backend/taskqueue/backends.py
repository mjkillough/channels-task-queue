#!/usr/bin/env python

from . import models


class Backend:
    """Interface that all task-queue backends must implement."""

    def __init__(self):
        self.registry = {}

    def register_task(self, task):
        """Registers the given task, so it can be referred to by name.

        A task must be registered before it can be run.
        Sub-classes shouldn't need to implement this function.

        :params task: The `taskqueue.Task` to register.
        """
        self.registry[task.name] = task

    def get_task_by_name(self, task_name):
        """Returns the registered task with the given name.

        Sub-classes shouldn't need to implement this function.

        :param task_name: The name of the task to be retrieved from the registry.
        :returns: The `taskqueue.Task`.
        :raises: KeyError if the task can not be found.
        """
        return self.registry[task_name]

    def push_task(self, task, params):
        """Enqeues a task to be run in the background.

        Enqeues a task with the given positional arguments. (Keyword arguments
        are not currently supported). Returns the ID of the enqueud task, which
        can later be used to get its status.

        :param task: The `taskqueue.Task` to be run.
        :param params: A list of positional parameters to be passed to the task.
        :returns: An opaque identifier for the task.
        """
        pass

    def pop_task(self):
        """Pops a (task, params) tuple from the task queue.

        For internal use by the task worker.

        :returns: A tuple of the task and its positional arguments.
        :rtype: (`taskqueue.Task`, list)
        """
        pass

    def context_for_task_id(self, id):
        """Given a task's ID, returns its TaskContext.

        The TaskContext can be used to get information about the task, such as
        its status, progress, or result. Callers can use the
        `.refresh()` method on the returned model to get the latest state.

        :param id: The ID of the task, as returned by `push_task`.
        :returns: The `TaskContext` model for the task.
        """
        pass


# The backend to be used by the application.
# TODO: Instantiate this dynamically based on the Django app's settings.
backend = Backend()
