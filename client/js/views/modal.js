var Backbone = require('backbone');


var ModalView = Backbone.View.extend({
  events: {

  },

  initialize: function() {
    this.closable = true;
  },

  close: function() {
    this.trigger('close');
  }
});

module.exports = ModalView;