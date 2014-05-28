var _ = require('underscore');
var Pikaday = require('pikaday');

var ModalView = require('./modal');
var AreaSelectView = require('./areaselect');


var EventModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {

  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);

    this.load(options.url).done(function() {
      var areaSelect = new AreaSelectView({ el: $('.js-area-select') });
      this.$('.js-datepicker').each(function() {
        new Pikaday({ field: this });
      });
    }.bind(this));
  }
});

module.exports = EventModalView;