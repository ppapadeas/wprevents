var _ = require('underscore');

var FormModalView = require('./formmodal');

var ImportModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {
    'click .js-close': 'closeAndReload',
    'click .js-button': 'onClickButton'
  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    this.$content = this.$('.js-content');
    this.$spinner = $('<div class="spinner"></div>');
  },

  onClickButton: function(e) {
    this.clearErrors();
    this.closable = false;
    this.$spinner.insertAfter($(e.target));
  },

  onError: function(errors) {
    FormModalView.prototype.onError.call(this, errors);
    this.closable = true;
    this.$spinner.remove();
  },

  onSuccess: function(response) {
    var $message = $('<p class="import-success">'+ response.message +'</p><div class="row"><a class="button js-close" href="#">Ok</a></div>');
    this.$content.replaceWith($message);
    this.closable = true;
    this.$spinner.remove();
  },

  closeAndReload: function() {
    if (this.closable) {
      this.close();
      window.location.reload();
    }
  }
});

module.exports = ImportModalView;