// import { useService } from "@web/core/utils/hooks";
//
// export const useNotificationHandler = (env) => {
//     const notificationService = useService("notification");
//     const bus = useService("bus_service");
//     bus.addChannel("your_channel_name");
//     bus.addEventListener("notification", (ev) => {
//         console.log("Notification Event Received:", ev);
//     console.log("ev.detail:", ev.detail);
//         ev.detail
//             .filter(notif => notif.type === "your_channel_name")
//             .forEach(({ payload }) => {
//                 this.notificationService.add(payload.message, {
//                     title: payload.title,
//                     type: payload.type,
// });
//             });
//     });
// };

odoo.define('VATSync.notification_listener', function (require) {
    "use strict";

    var bus = require('bus.Longpolling');  // Try requiring bus.Longpolling
    var core = require('web.core');

    // Start bus polling
    bus.startPolling();

    // Listen for notifications
    bus.on('notification', null, function (notifications) {
        _.each(notifications, function (notification) {
            var channel = notification[0];  // This is your channel name
            var message = notification[1];  // This is the message payload

            if (channel === 'your_channel_name') {
                console.log("Notification received: ", message);
            }
        });
    });
});
