var $ = require('jquery');
var Backbone = require('backbone');

Backbone.$ = $;

var MapView = require('./views/map');

var ScreenView = Backbone.View.extend({
  events: {
    'click .js-event': 'onEventClick'
  },

  initialize: function() {
    this.$events = $('.js-event');
    this.$details = $('.js-event-info');
    this.selectFirstRow();

    var map = new MapView({ el: '#map', hideControls: true, dragging: false, markerOffset: { x: -($(window).width() * 0.25), y: -50 } });
    map.on('ready', function() {
      map.focusSpace(map.$el.data('space'));
    });

    setTimeout(this.refresh.bind(this), 30000);
  },

  selectFirstRow: function() {
    this.currentEventId = this.$events.first().data('id');
    this.selectEvent(this.currentEventId);
  },

  reset: function() {
    this.setElement($('.js-screen-content'));
    this.$events = $('.js-event');
    this.$details = $('.js-event-info');
    this.selectEvent(this.currentEventId);
  },

  onEventClick: function(e) {
    var $row = $(e.target).closest('.js-event');
    this.currentEventId = $row.data('id');
    this.selectEvent(this.currentEventId);

    // prevent going to event page if link is clicked
    e.preventDefault();
  },

  selectEvent: function(id) {
    var eventExists = false;

    this.$events.removeClass('active');
    this.$events.each(function() {
      if ($(this).data('id') === id) {
        $(this).addClass('active');
        eventExists = true;
      }
    });

    if (eventExists) {
      this.showEventDetails(id);
    } else {
      this.selectFirstRow();
    }
  },

  showEventDetails: function(id) {
    this.$details.removeClass('active');
    this.$details.each(function() {
      if ($(this).data('id') === id) {
        $(this).addClass('active');
      }
    });
  },

  refresh: function() {
    setTimeout(this.refresh.bind(this), 30000);
    $.ajax({
      url: window.location,
      success: function(data) {
        var $content = $(data).find('.js-screen-content');
        this.$el.replaceWith($content);
        this.reset();
      }.bind(this)
    });
  }
});

new ScreenView({ el: $('.js-screen-content') });