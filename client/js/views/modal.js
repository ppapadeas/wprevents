var Backbone = require('backbone');


var ModalView = Backbone.View.extend({
  events: {

  },

  initialize: function() {
    this.$container = $('.modal-container');
    this.$container.on('click', this.onClickContainer.bind(this));
  },

  onClickContainer: function(e) {
    var $target = $(e.target);
    var modal = this.$container.find('.modal')[0];

    if (!$target.parents('.modal-container').length > 0) {
      this.close();
    }

  },

  load: function(path) {
    $.get(path).done(function(html) {
      this.$container.removeClass('disabled');
      this.$container.append(html);
    }.bind(this));
  },

  close: function() {
    this.$container.addClass('disabled');
    this.$container.html('');
  }
});

module.exports = ModalView;