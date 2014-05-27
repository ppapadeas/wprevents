var Backbone = require('backbone');
var CalendarEventView = require('./calendarevent');

var CalendarView = Backbone.View.extend({
  events: {

  },

  initialize: function() {
    this.$events = this.$('.js-event');
    $.each(this.$events, function(i, el) {
      var view = new CalendarEventView({ el: el });
    });
  },

  update: function(filters) {
    console.log("Filtering event list with:", filters);

    // TODO: XHR to update event list
  }
});

module.exports = CalendarView;