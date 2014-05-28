var _ = require('underscore');

var ModalView = require('./modal');
var AreaSelectView = require('./areaselect');


var EventModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {

  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);

    this.load(options.url).done(function() {
      var areaSelect = new AreaSelectView({ el: $('.js-area-select') });
    });
  }
});

module.exports = EventModalView;