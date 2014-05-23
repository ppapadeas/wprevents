var Backbone = require('backbone');

var EventListView = Backbone.View.extend({
  initialize: function() {
    this.$events = this.$('.event');
  },

  update: function(filters) {
    console.log("Filtering event list with:", filters);

    // TODO: XHR to update event list
  }
});

module.exports = EventListView;