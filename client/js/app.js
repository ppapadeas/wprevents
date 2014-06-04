var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');

Backbone.$ = $;

var MapView = require('./views/map');
var FiltersView = require('./views/filters');
var EventListView = require('./views/eventlist');
var CalendarView = require('./views/calendar');

var App = function() {
  var map = new MapView({ el: '#map' });
  var filters = new FiltersView({ el: '.filters-container' });
  var list = new EventListView({ el: '.js-event-list' });
  var calendar = new CalendarView({ el: '#js-calendar' });

  filters.on('change', function(filters) {
    list.update(filters);
    if (_.has(filters, 'space')) {
      map.selectMarker(filters.space);
    } else {
      map.deselectMarker();
    }
  });

  map.on('ready', function() {
    var id = $('.js-event-space').data('space');
    if (id) {
      map.focusSpace(id);
    }
  });

  map.on('markerClick', function(id) {
    filters.setSpace(id);
  });
};

$(function() {
  var app = new App();
});