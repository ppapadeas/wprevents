var Backbone = require('backbone');

var CalendarEventView = Backbone.View.extend({
  events: {
    "mouseenter": "onMouseEnter",
    "mouseleave": "onMouseLeave"
  },

  initialize: function() {
    this.$clone = '';
    this.topBorder = this.$el.parents('tr').prevAll().length === 0 ? 0 : 1;
    this.leftBorder = this.$el.parents('td').prevAll().length === 0 ? 0 : 1;
  },

  clone: function(e) {
    var $cell = this.$el.parents('td');
    $cell.offset.y = this.$el.offset().top - $cell.offset().top - this.topBorder;
    $cell.offset.x = this.$el.offset().left - $cell.offset().left - this.leftBorder;

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