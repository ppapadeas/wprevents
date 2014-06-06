var _ = require('underscore');

var FormModalView = require('./formmodal');

var AreaModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {

  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

  }
});

module.exports = AreaModalView;