var $ = require('jquery');
var Backbone = require('backbone');

Backbone.$ = $;

var MapView = require('./views/map');
var FiltersView = require('./views/filters');
var EventListView = require('./views/eventlist');
var CalendarView = require('./views/calendar');

var App = function() {
  var map = new MapView({ el: '#map' });
  var filters = new FiltersView({ el: '.filters-container' });
  var list = new EventListView({ el: '.event-list' });
  var calendar = new CalendarView({ el: '#js-calendar' });

  filters.on('change', function(filters) {
    list.update(filters);
  });
};

$(function() {
  var app = new App();
});