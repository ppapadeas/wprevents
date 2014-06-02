var _ = require('underscore');

var ModalView = require('./modal');


var FormModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {

  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);

    this.$form = this.$('form');
    this.$button = this.$('.js-button');
    this.$errors = this.$('.js-errors');

    this.$form.ajaxForm({
      beforeSubmit: function() {
        this.disableSubmitButton();
      }.bind(this),
      success: function(response) {
        if (response.status === 'error') {
          this.clearErrors();
          _.each(response.errors, this.addError.bind(this));
          this.enableSubmitButton();
        } else if (response.status === 'success') {
          window.location.reload();
        }
      }.bind(this)
    });
  },

  addError: function(error) {
    this.$errors.append($('<li>' + error + '</li>'));
  },

  clearErrors: function() {
    this.$errors.html('');
  },

  enableSubmitButton: function() {
    this.$button.prop("disabled", false);
  },

  disableSubmitButton: function() {
    this.$button.prop("disabled", true);
  }
});

module.exports = FormModalView;