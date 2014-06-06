var _ = require('underscore');

var FormModalView = require('./formmodal');

var AreaModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {
    'click .js-close': 'closeAndReload'
  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    this.$content = this.$('.js-content');

  },

  onSuccess: function(response) {
    var $message = $('<p class="import-success">'+ response.message +'</p><div class="row"><a class="button js-close" href="#">Ok</a></div>');
    this.$content.replaceWith($message);
  },

  closeAndReload: function() {
    this.close();
    window.location.reload();
  }
});

module.exports = AreaModalView;