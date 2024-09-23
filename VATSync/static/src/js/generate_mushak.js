odoo.define('your_module.open_url_with_auth', function (require) {
    "use strict";

    var core = require('web.core');

    core.action_registry.add('open_url_with_auth', function (action) {
        var url = action.url;
        var headers = action.headers;

        // Create a hidden form to submit the request with headers
        var form = document.createElement('form');
        form.method = 'POST';
        form.action = url;
        form.target = '_blank';

        // Add headers as hidden inputs
        for (var key in headers) {
            if (headers.hasOwnProperty(key)) {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = headers[key];
                form.appendChild(input);
            }
        }

        // Submit the form
        document.body.appendChild(form);
        form.submit();
        document.body.removeChild(form);
    });
});