#!/usr/bin/env python
# encoding: utf-8

import django.test

from .. import backends


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
