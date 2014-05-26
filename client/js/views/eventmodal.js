var _ = require('underscore');

var ModalView = require('./modal');


var EventModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {

  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);

    this.load(options.url);
  }
});

module.exports = EventModalView;