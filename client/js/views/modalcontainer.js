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

  loadModal: function(ModalType, path) {
    var topMargin = 150;
    var scrollTop = $(window).scrollTop();

    // Load HTML via HXR then create the view object asynchronously
    return $.get(path).done(function(html) {
      this.$el.html(html);
      this.showBackground();

      this.modal = new ModalType({ el: this.$('.js-modal') });
      this.modal.$el.css('marginTop', topMargin + scrollTop);
      this.modal.on('close', this.closeCurrentModal.bind(this));
    }.bind(this)).pipe(function() {
      return this.modal;
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