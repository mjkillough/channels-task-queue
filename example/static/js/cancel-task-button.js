'use strict';

(function() {

    // <cancel-task> component, which allows a user to start cancel a running
    // task and shows 'Canceling' while we wait for a canceled task to stop.
    Vue.component('cancel-task-button', {
        template: '#tmpl-cancel-task-button',

        props: ['task'],

        computed: {
            canceling: function() {
                return this.task !== null && this.task.canceling;
            },

            canceled: function() {
                return (
                    this.task !== null &&
                    this.task.status === TASK_STATUS.Canceled
                );
            },

            canCancel: function() {
                return (
                    this.task !== null &&
                    !this.canceling &&
                    !TASK_FINISHED_STATES.includes(this.task.status)
                );
            },

            buttonText: function() {
                return this.canceled  ? 'Canceled' :
                       this.canceling ? 'Canceling...'
                                      : 'Cancel';
            },
        },

        methods: {
            cancel: async function() {
                if (this.task === null) {
                    console.warn('Tried to cancel() without a task!')
                    return;
                }

                const resp = await fetch('/cancel/' + this.task.id + '/');
                const json = await resp.json();
                console.assert(json.success);

                // We _could_ propogate the new json to the parent component
                // using an event. (Or a state store, if we had one...) However,
                // for simplicity, don't. This means there's a brief window
                // where the 'Cancel' button will become re-enabled.
            },
        },
    });

})();
