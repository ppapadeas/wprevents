var Backbone = require('backbone');

var CalendarEventView = Backbone.View.extend({
  events: {
    "mouseenter": "onMouseEnter",
    "mouseleave": "onMouseLeave"
  },

  initialize: function() {
    this.$clone = '';
  },

  clone: function(e) {
    var $cell = this.$el.parents('td');
    $cell.offset.y = this.$el.offset().top - $cell.offset().top;
    $cell.offset.x = this.$el.offset().left - $cell.offset().left - 1; // we remove 1px to account for the cell border

    var $clone = this.$el.clone();
    $clone.addClass('tooltip');
    $clone.css({
      position: 'absolute',
      top: $cell.offset.y,
      left: $cell.offset.x
    });
    $cell.append($clone);

    this.$clone = $clone;
  },

  onMouseEnter: function(e) {
    if (this.$clone.length === 0) {
      this.clone();
    }
  },

  onMouseLeave: function(e) {
    this.$clone.remove();
    this.$clone = '';
  }
});

module.exports = CalendarEventView;