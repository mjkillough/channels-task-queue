#!/usr/bin/env python
# encoding: utf-8


def run_task_consumer(msg):
    print(msg['id'])
    print(msg['name'])
    print(msg['parameters'])
