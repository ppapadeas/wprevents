var Backbone = require('backbone');


var ModalView = Backbone.View.extend({
  events: {

  },

  initialize: function() {
    this.$container = $('.modal-container');
  },

  load: function(path) {
    $.get(path).done(function(html) {
      this.$container.removeClass('disabled');
      this.$container.append(html);
    }.bind(this));
  },

  close: function() {
    this.$container.addClass('disabled');
  }
});

module.exports = ModalView;