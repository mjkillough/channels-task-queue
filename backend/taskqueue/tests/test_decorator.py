#!/usr/bin/env python
# encoding: utf-8

import unittest

import django.test

from .. import backends, decorator


# For use by the tests. It's easier if they're module-level, due to our use
# of __name__.
def dummy_func1(arg1, arg2):
    pass


# Wrap tests or classes with this to have a MagicMock for a Backend.
mocked_backend = unittest.mock.patch('taskqueue.backends.backend')


@mocked_backend
class TaskDecoratorTests(django.test.TestCase):

    def test_decorator_gives_task(self, backend):
        task = decorator.task()(dummy_func1)
        self.assertEqual(task.__class__, decorator.Task)
        self.assertEqual(task.name, dummy_func1.__name__)
        self.assertEqual(task.func, dummy_func1)

    def test_decorator_registers_with_backend(self, backend):
        task = decorator.task()(dummy_func1)
        backend.register_task.assert_called_with(task)

    @unittest.skip('Not Implemented')
    def test_decorator_checks_arity(self, backend):
        task = decorator.task()(dummy_func1)
        with self.assertRaises(Exception):
            task.call_async(1, 2, 'too many args')

