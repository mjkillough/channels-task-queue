'use strict';

(function() {

    // <dummy-task-runner> component, which allows a user to start our task,
    // watch its progress and cancel its execution.
    Vue.component('dummy-task-runner', {
        template: '#tmpl-dummy-task-runner',

        data: () => {
            return {
                pollIntervalMs: 100,
                task: null,
            };
        },

        computed: {
            havePendingTask: function() {
                return (
                    this.task !== null &&
                    !TASK_FINISHED_STATES.includes(this.task.status)
                );
            },
        },

        methods: {
            startTask: async function() {
                const resp = await fetch('/start/');
                const json = await resp.json();
                console.assert(json.success);
                this.task = json.task;

                // Set off our polling of task status, which will continue
                // until the task is no longer pending.
                setTimeout(this.pollTaskStatus, this.pollIntervalMs);
            },

            pollTaskStatus: async function() {
                if (!this.havePendingTask) {
                    return;
                }

                const resp = await fetch('/task/' + this.task.id + '/');
                const json = await resp.json();
                console.assert(json.success);
                this.task = json.task;

                // Call ourselves again after poll interval. If we find
                // ourselves without a pending task, we'll stop updating.
                setTimeout(this.pollTaskStatus, this.pollIntervalMs);
            },
        },
    });

})();
