var Backbone = require('backbone');


var ModalContainerView = Backbone.View.extend({
  events: {
    'mousedown': 'closeOnOutsideClick'
  },

  initialize: function() {

  },

  closeOnOutsideClick: function(e) {
    if (this.modal && this.$el.is(e.target) && this.modal.closable) {
      this.closeCurrentModal();
    }
  },

  showBackground: function() {
    this.$el.removeClass('disabled');
  },

  hideBackground: function() {
    this.$el.addClass('disabled');
  },

  empty: function() {
    this.$el.html('');
  },

  setCurrentModal: function(ModalType, path) {
    // Load HTML then create view object asynchronously
    $.get(path).done(function(html) {
      this.$el.html(html);
      this.showBackground();

      this.modal = new ModalType({ el: this.$('.js-modal') });
      this.modal.on('close', this.closeCurrentModal.bind(this));
    }.bind(this));
  },

  closeCurrentModal: function() {
    this.hideBackground();
    this.empty();
    this.modal.remove();
    this.modal = null;
  }
});

module.exports = ModalContainerView;