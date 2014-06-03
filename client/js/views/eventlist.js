var Backbone = require('backbone');

var EventListView = Backbone.View.extend({
  initialize: function() {
    this.$events = this.$('.event');

    this.token = $("form [name='csrfmiddlewaretoken']").val();
  },

  update: function(filters) {
    $.ajax({
      url: "/search?" + $.param(filters),
      type: "GET",
      beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", this.token);
      }.bind(this),
      success: function(html) {
        this.$el.html(html);
      }.bind(this)
    });
  }
});

module.exports = EventListView;