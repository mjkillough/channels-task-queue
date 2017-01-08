#!/usr/bin/env python
# encoding: utf-8

import json
import unittest

import django.test

from .. import backends, models


class DummyTask:
    """Something like a Task that doesn't register itself."""
    def __init__(self, name):
        self.name = name


class BackendRegistryTests(django.test.TestCase):
    """Test tasks can be registered and retrieved from the backend."""

    def test_register_and_retrieve(self):
        backend = backends.Backend()
        task = DummyTask('task1')
        backend.register_task(task)
        self.assertEqual(backend.get_task_by_name('task1'), task)

    def test_register_same_name_twice(self):
        # Should return the most recently registered.
        # We don't expect this will happen often, but best that it be deterministic.
        backend = backends.Backend()
        task1 = DummyTask('task')
        task2 = DummyTask('task')
        backend.register_task(task1)
        backend.register_task(task2)
        self.assertEqual(backend.get_task_by_name('task'), task2)

    def test_retrieve_nonexistent(self):
        backend = backends.Backend()
        with self.assertRaises(KeyError):
            backend.get_task_by_name('task')


class ChannelsBackendTests(django.test.TestCase):

    def setUp(self):
        super().setUp()
        self.backend = backends.ChannelsBackend()
        self.channel = self.backend.channel = unittest.mock.Mock()

    def test_push_task_sent_to_channel(self):
        task = DummyTask('name')
        id = self.backend.push_task(task, [1, 2])
        self.channel.send.assert_called_once_with(dict(
            id=id,
            name=task.name,
            parameters=[1, 2]
        ))

    def test_push_task_saved_to_db(self):
        """Checks a TaskContext is created for the task and saved to the DB."""
        task = DummyTask('name')
        id = self.backend.push_task(task, [1, 2])
        self.assertTrue(models.TaskContext.objects.filter(id=id).exists())

        task_context = models.TaskContext.objects.get(id=id)
        self.assertEqual(task_context.status, models.TaskContext.TaskStatus.Queued)
        self.assertEqual(task_context.parameters_json, json.dumps([1, 2]))
