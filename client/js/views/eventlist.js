var Backbone = require('backbone');

var EventListView = Backbone.View.extend({
  events: {
    "mouseenter .js-event": 'onMouseEnterEvent',
    "mouseleave .js-event": 'onMouseLeaveEvent'
  },

  initialize: function() {
    this.$events = this.$('.js-event');

    this.token = $("form [name='csrfmiddlewaretoken']").val();
  },

  onMouseEnterEvent: function(e) {
    var space = $(e.target).closest('.js-event').data('space');
    this.trigger('mouseEnterEvent', space);
  },

  onMouseLeaveEvent: function(e) {
    var space = $(e.target).closest('.js-event').data('space');
    this.trigger('mouseLeaveEvent', space);
  },

  update: function(filters) {
    this.$el.css('height', this.$el.height());
    this.$el.addClass('loading');

    $.ajax({
      url: "/filter_list?" + $.param(filters),
      type: "GET",
      beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", this.token);
      }.bind(this),
      success: function(html) {
        this.$el.html(html);
        this.$el.removeClass('loading');
        this.$el.removeAttr('style');
      }.bind(this)
    });
  },

  show: function() {
    this.$el.removeClass('hidden');
  },

  hide: function() {
    this.$el.addClass('hidden');
  }
});

module.exports = EventListView;