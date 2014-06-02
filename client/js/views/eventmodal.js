var _ = require('underscore');
var Pikaday = require('pikaday');

var FormModalView = require('./formmodal');
var AreaSelectView = require('./areaselect');


var EventModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {

  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    this.areaSelect = new AreaSelectView({ el: $('.js-area-select') });
    this.$('.js-datepicker').each(function() {
      new Pikaday({ field: this });
    });
  }
});

module.exports = EventModalView;