var Backbone = require('backbone');

var AreaSelectView = Backbone.View.extend({
  events: {
    "focusin .areas-select": "onFocus",
    "mousedown .areas-select": "onFocus",
    "change input": "onChange"
  },

  initialize: function() {
    this.$select = this.$('.areas-select');
    this.$list = this.$('.areas-dropdown');
    this.$option = this.$select.find('option');
    this.selectPlaceholderText = this.$option.html();

    $(window).on('click', function(e) {
      if (!$(e.target).parents('.areas-dropdown').length > 0) {
        this.close();
      }
    }.bind(this));
  },

  onFocus: function(e) {
    e.preventDefault();

    this.open();
  },

  open: function() {
    this.$list.removeClass('hidden');
  },

  close: function() {
    this.$list.addClass('hidden');
  },

  onChange: function() {
    var areas = [];
    this.$('input:checked').each(function(i, el) {
      var name = i === 0 ? $(el).parent('label').text() : ', ' + $(el).parent('label').text();
      areas.push(name);
    });
    this.update(areas);
  },

  update: function(areas) {
    if (areas.length > 0) {
      this.$option.html(areas);
    } else {
      this.$option.html(this.selectPlaceholderText);
    }

  }
});

module.exports = AreaSelectView;