odoo.define('your_module_name.tour', function (require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');

    tour.register('vat_bangladesh_tour', {
        url: "/web",
        rainbowMan: true,
        sequence: 5,
    }, [
        {
            trigger: '.o_app[data-menu-xmlid="sale.sale_menu_root"]',
            content: 'Open the Sales app to start the VAT Bangladesh tour.',
            position: 'bottom',
        },
        // The tour steps will be automatically loaded from the XML definition
    ]);
});