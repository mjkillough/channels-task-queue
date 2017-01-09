'use strict';

(function() {

    // <progress-bar> component, which does exactly what you think it'll do.
    // Accepts one property 'percent' which we expect to be an integer
    // between 0 and 100.
    Vue.component('progress-bar', {
        template: '#tmpl-progress-bar',

        props: {
            percent: {
                validator: (value) => value >= 0 && value <= 100
            }
        }
    });

})();
