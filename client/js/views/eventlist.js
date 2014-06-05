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
        if (html.length > 0) {
          this.$el.html(html);
        } else {
          this.$el.html('<div class="billboard no-events-found">No events found</div>');
        }
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