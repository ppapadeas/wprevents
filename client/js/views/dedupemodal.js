var _ = require('underscore');

var ModalView = require('./modal');


var DedupeModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {

  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);
  }
});

module.exports = DedupeModalView;