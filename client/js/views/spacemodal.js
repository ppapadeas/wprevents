var _ = require('underscore');

var FormModalView = require('./formmodal');

var SpaceModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {

  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    console.log('Space modal view initalized');
  }
});

module.exports = SpaceModalView;