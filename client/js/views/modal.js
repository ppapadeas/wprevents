var Backbone = require('backbone');


var ModalView = Backbone.View.extend({
  events: {

  },

  initialize: function() {
    this.$container = $('.modal-container');
    this.$container.on('mousedown', this.onClickContainer.bind(this));
  },

  onClickContainer: function(e) {
    var $target = $(e.target);
    var modal = this.$container.find('.modal')[0];

    if (!$target.parents('.modal-container').length > 0) {
      this.close();
    }

  },

  load: function(path) {
    return $.get(path).done(function(html) {
      this.$container.removeClass('disabled');
      this.$container.append(html);
      this.setElement(this.$container.find('.modal'));
    }.bind(this));
  },

  close: function() {
    this.$container.addClass('disabled');
    this.$container.html('');
  }
});

module.exports = ModalView;