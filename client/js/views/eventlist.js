var Backbone = require('backbone');

var EventListView = Backbone.View.extend({
  initialize: function() {
    this.$events = this.$('.event');

    this.token = $("form [name='csrfmiddlewaretoken']").val();
  },

  update: function(filters) {
    this.$el.css('height', this.$el.height());
    this.$el.addClass('loading');

    $.ajax({
      url: "/search?" + $.param(filters),
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