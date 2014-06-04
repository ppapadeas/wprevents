var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');

Backbone.$ = $;

var MapView = require('./views/map');
var FiltersView = require('./views/filters');
var EventListView = require('./views/eventlist');
var CalendarView = require('./views/calendar');
var TabsView = require('./views/tabs');


var App = Backbone.Router.extend({
  routes: {
    '': 'list', // index page is on list tab by default
    'calendar': 'calendar'
  },

  initialize: function() {
    this.views = {
      map: new MapView({ el: '#map' }),
      filters: new FiltersView({ el: '.filters-container' }),
      tabs: new TabsView({ el: '.main-tabs' }),
      list: new EventListView({ el: '.js-event-list' }),
      calendar: new CalendarView({ el: '.js-calendar' })
    };

    this.views.tabs.on('navigate', function(path) {
      this.navigate(path, { trigger: true });
    }, this);

    this.views.map.on('ready', function() {
      var id = $('.js-event-space').data('space');
      if (id) {
        this.views.map.focusSpace(id);
      }
    }, this);

    this.views.map.on('markerClick', function(id) {
      this.views.filters.setSpace(id);
    }, this);

    this.views.filters.on('change', function(filters) {
      this.views.list.update(filters);
      this.views.calendar.update(filters);

      if (_.has(filters, 'space')) {
        this.views.map.selectMarker(filters.space);
      } else {
        this.views.map.deselectMarker();
      }      
    }, this);
  },

  list: function() {
    this.views.tabs.activate('list');
    this.views.list.show();
    this.views.calendar.hide();
  },

  calendar: function() {
    this.views.tabs.activate('calendar');
    this.views.list.hide();
    this.views.calendar.show();
  }
});

$(function() {
  new App();
  Backbone.history.start({ pushState: true });
});

