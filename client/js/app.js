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
    '': 'listTab', // index page is on list tab by default
    'calendar': 'calendarTab',
    'e/:id/:slug': 'eventPage'
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
      this.zoomOnSpace();
    }, this);

    // Clicking on a space pin on the map updates the space filter value
    this.views.map.on('markerClick', function(id) {
      this.views.filters.setSpace(id);
    }, this);

    // Changing a filter updates events in both list and calendar tabs
    this.views.filters.on('change', function(filters) {
      this.views.list.update(filters);
      this.views.calendar.update(filters);

      // If the space filter has a non-default value,
      // the corresponding space pin is selected on the map.
      if (_.has(filters, 'space')) {
        this.views.map.selectMarker(filters.space);
      } else {
        this.views.map.deselectMarker();
      }
    }, this);

    // Hovering over event rows in the list tab highlights space pins
    this.views.list.on('mouseEnterEvent', function(space) {
      this.views.map.highlightMarker(space);
    }, this);

    this.views.list.on('mouseLeaveEvent', function(space) {
      this.views.map.unHighlightAllMarkers(space);
    }, this);

    // Clicking on an event link in the list tab shows an event page
    this.views.list.on('showEvent', function(url) {
      this.navigate(url, { trigger: true });
    }, this);

    // Clicking on a calendar day number displays all events
    // of this day in the list tab. Both date filters are 
    // also automatically set to this day.
    this.views.calendar.on('filterDate', function(date) {
      this.views.filters.setDates(date);
      this.views.filters.refresh();
      this.navigate('', { trigger: true });
    }, this);

    // Clicking on a calendar event shows an event page
    this.views.calendar.on('showEvent', function(url) {
      this.navigate(url, { trigger: true });
    }, this);

    // Clicking on the logo resets to the list tab with no filters
    $('.js-home').on('click', function(e) {
      e.preventDefault();

      this.views.filters.reset();
      this.views.filters.refresh();
      this.navigate('', { trigger: true });
    }.bind(this));
  },

  zoomOnSpace: function() {
    var id = $('.js-event-space').data('space');

    if (id) {
      this.views.map.focusSpace(id);
    }
  },

  resetMap: function() {
    this.views.map.setDefaultState();
  },

  showEventPage: function() {
    $('.js-event-container').show();
    $('.js-filters-container').hide();
    $('.js-tabs-container').hide();
  },

  hideEventPage: function() {
    this.isEventShown = false;
    $('.js-event-container').hide();
    $('.js-filters-container').show();
    $('.js-tabs-container').show();
  },

  // Routes

  listTab: function() {
    this.views.tabs.activate('list');
    this.views.list.show();
    this.views.calendar.hide();
    this.views.filters.enableDateFilters();
    this.hideEventPage();
    this.resetMap();
  },

  calendarTab: function() {
    this.views.tabs.activate('calendar');
    this.views.list.hide();
    this.views.calendar.show();
    this.views.filters.disableDateFilters();
    this.hideEventPage();
    this.resetMap();
  },

  eventPage: function(id, slug) {
    if (!this.isEventShown) {
      $.ajax({
        url: window.location,
        success: function(data) {
          var $el = $(data).find('.js-event-container');

          $('.js-filters-container').hide();
          $('.js-tabs-container').hide();

          if (this.$currentEvent) {
            this.$currentEvent.remove();
          }

          this.isEventShown = true;
          this.$currentEvent = $el;

          window.scrollTo(0, 0);
          $('#inner-wrapper').children().last().after($el);
          this.zoomOnSpace();
        }.bind(this)
      });
    } else {
      this.showEventPage();
    }
  }
});

$(function() {
  new App();
  Backbone.history.start({ pushState: true, silent: true });
});

