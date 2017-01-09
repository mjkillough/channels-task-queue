'use strict';

// Make these global for now, in a real project these would be in a module
// somewhere.

var TASK_STATUS = {
    Queued: 1,
    Running: 2,
    Canceled: 3,
    Failed: 4,
    Complete: 5,
};

// States that indicate the task has finished executing.
var TASK_FINISHED_STATES = [
    TASK_STATUS.Canceled, TASK_STATUS.Failed, TASK_STATUS.Complete,
]
