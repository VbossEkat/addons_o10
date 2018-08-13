/**
 * Created by boss on 2017/07/23.
 */
openerp.sba_db_mang_debrand = function(instance) {
// меняем заголовок закладки в броузере
	instance.web.WebClient.include({
	    init: function(parent, client_options) {
            this._super(parent, client_options);
            this.set('title_part', {"zopenerp": 'SBA1'});
            console.log("000000000000");
        },
    })
},
odoo.sba_db_mang_debrand = function(instance) {
// меняем заголовок закладки в броузере
	instance.web.WebClient.include({
	    init: function(parent, client_options) {
            this._super(parent, client_options);
            this.set('title_part', {"zopenerp": 'SBA2'});
            console.log("1111111111111111");
        },
    })
}