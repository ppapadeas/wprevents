var Backbone = require('backbone');

var ColorPickerView = Backbone.View.extend({
  events: {
    'click .js-button': 'open',
    'click .js-swatch': 'chooseSwatch'
  },

  initialize: function() {
    this.$button = this.$('.js-button');
    this.$dropdown = this.$('.js-dropdown');
    this.$input = this.$('.js-color-input');

    $(window).on('click', function(e) {
      if (!$(e.target).parents('.js-color-picker').length > 0) {
        this.close();
      }
    }.bind(this));
  },

  chooseSwatch: function(e) {
    var color = $(e.target).data('value');
    this.update(color);
    this.close();
  },

  open: function() {
    this.$dropdown.removeClass('hidden');
  },

  close: function() {
    this.$dropdown.addClass('hidden');
  },

  update: function(color) {
    this.$button.removeAttr('class').addClass('selected-swatch js-button ' + color);
    this.$input.val(color);
  }
});

module.exports = ColorPickerView;