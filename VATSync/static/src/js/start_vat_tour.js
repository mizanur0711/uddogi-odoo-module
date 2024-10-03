odoo.define('VATSync.tour', function (require) {
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
        {
            trigger: 'a[data-menu-xmlid="VATSync.menu_vat_bangladesh"]',
            content: 'Click here to access the VAT Bangladesh wizard for date range selection.',
            position: 'bottom'
        },
        {
            trigger: 'button[name="action_generate_mushak_pdf"]',
            content: 'Click here to generate the VAT 6.3 Report through the VAT Bangladesh Calculation engine.',
            position: 'bottom'
        }
    ]);
});
