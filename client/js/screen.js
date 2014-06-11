var $ = require('jquery');
var Backbone = require('backbone');

Backbone.$ = $;

var ScreenView = Backbone.View.extend({
  events: {
    'click .js-event': 'selectEvent'
  },

  initialize: function() {
    this.$events = $('.js-event');
    this.$details = $('.js-event-info');
    this.$events.eq(0).addClass('active');
    this.showEventDetails(0);
  },

  selectEvent: function(e) {
    var $el = $(e.target).closest('.js-event');
    var index = $el.prevAll('.js-event').length;
    this.$events.removeClass('active');
    $el.addClass('active');

    this.showEventDetails(index);
  },

  showEventDetails: function(index) {
    this.$details.removeClass('active');
    this.$details.eq(index).addClass('active');
  }
});

new ScreenView({ el: $('.screen-content') });