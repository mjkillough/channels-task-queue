# Channels Task Queue — `taskqueue`

An experimental, incomplete task queue for [Django Channels](https://channels.readthedocs.io/en/stable/). It is not recommended for actual use and is not packaged as a re-usable Django application for a reason!

An example of its usage:

```python
import time
import taskqueue

@taskqueue.task()
def dummy_sleeping_task(task, total_time_in_seconds):
    sleep_period = 2 # seconds
    total_sleep_ticks = math.ceil(total_time_in_seconds / sleep_period)
    for tick in range(total_sleep_ticks):
        progress = (tick / total_sleep_ticks) * 100
        task.set_progress(progress)
        print('Tick %i: %i' % (task.id, progress))
        time.sleep(sleep_period)


# To run:
task_context = dummy_sleeping_task.call_async(30)
task_context.refresh()
print(task_context.status)
print(task_context.progress)
task_context.cancel()
time.sleep(2)
task_context.refresh()
print(task_context.status)
```

(This example is expanded upon in `backend/`).

Future work:
- A simple front-end that utilises the views exposed in `backend/` to give an example of its usage.
- Complete the tests. Some are stubbed-out as comments, others are missing entirely.
- Address TODOs throughout the code.
- Allow keyword arguments to be passed to tasks.
- (Maybe) allow task arguments that can not be serialized to JSON.
- (Maybe) allow task return values that can not be serialized to JSON.
- Use Django Channels' new 'Data Binding' framework to stream changes to `TaskContext` (task progress) over a WebSocket, so that the front-end does not have to poll the server.


## Dependencies

Python 3. Other requirements are in `requirements.txt`, as usual:

```sh
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```


## Run

Set up the `virtualenv` and then:

```python
python manage.py migrate
python manage.py runserver
```

Then:
- Visit http://localhost:8000/start/ - this will start a task and return an ID.
- Visit http://localhost:8000/task/IDHERE/ - this will return task progress.
- Visit http://localhost:8000/cancel/IDHERE/ - this will cancel a running task.


## Tests

Run:

```sh
python manage.py test
```


## License

MIT
