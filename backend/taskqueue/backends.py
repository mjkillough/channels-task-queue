#!/usr/bin/env python

import json

import channels
import django.db.transaction

from . import models


class Backend:
    """Interface that all task-queue backends must implement.

    This isn't quite as generic as I'd hoped it'd be. I was imagining we'd
    expose a `pop_task()` that backends would need to implement. However, for
    a Channels backend, we don't need it at all, as we can just rely on
    Channel's built-in routing. Re-consider this interface if/when we come to
    add another type of backend.
    """

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
        raise NotImplemented('Should be implemented by sub-class')

    def context_for_task_id(self, id):
        """Given a task's ID, returns its TaskContext.

        The TaskContext can be used to get information about the task, such as
        its status, progress, or result. Callers can use the
        `.refresh()` method on the returned model to get the latest state.

        Sub-classes shouldn't need to implement this function.

        :param id: The ID of the task, as returned by `push_task`.
        :returns: The `TaskContext` model for the task.
        """
        return models.TaskContext.objects.get(id=id)


class ChannelsBackend(Backend):

    def __init__(self):
        super().__init__()
        self.channel = channels.Channel('taskqueue.queue')

    def push_task(self, task, params):
        with django.db.transaction.atomic():
            task_context = models.TaskContext.objects.create(
                status=models.TaskContext.TaskStatus.Queued,
                parameters_json=json.dumps(params),
            )

        self.channel.send(dict(
            id=task_context.id,
            name=task.name,
            parameters=params
        ))

        return task_context.id


# The backend to be used by the application.
# TODO: Instantiate this dynamically based on the Django app's settings.
backend = ChannelsBackend()
