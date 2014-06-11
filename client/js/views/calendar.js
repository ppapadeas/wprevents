var Backbone = require('backbone');
var _ = require('underscore');
var CalendarEventView = require('./calendarevent');

var CalendarView = Backbone.View.extend({
  events: {
    'click .js-prev': 'showPreviousMonth',
    'click .js-next': 'showNextMonth',
    'click .js-day':  'showEventsOfDay'
  },

  initialize: function() {
    this.$prev = this.$('.js-prev');
    this.$next = this.$('.js-next');
    this.$title = this.$('.js-title');
    this.$wrapper = this.$('.js-wrapper');
    this.$content = this.$('.js-content');
    this.$nav = this.$('.js-cal-nav');

    this.filters = {};
    this.isSliding = false;

    this.initEventViews();
  },

  getMonth: function(year, month) {
    var filters = _.clone(this.filters);

    // Ignore start date and end date filters in calendar
    delete filters.start;
    delete filters.end;

    // Add calendar-specific filters
    filters.year = year;
    filters.month = month;

    return $.get('/filter_calendar?' + $.param(filters));
  },

  getNextMonth: function() {
    return this.getMonth(this.$next.data('year'), this.$next.data('month'));
  },

  getPreviousMonth: function() {
    return this.getMonth(this.$prev.data('year'), this.$prev.data('month'));
  },

  showNextMonth: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.getNextMonth().done(function(html) {
        this.slide('forward', html);
      }.bind(this));
    }
  },

  showPreviousMonth: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.getPreviousMonth().done(function(html) {
        this.slide('backward', html);
      }.bind(this));
    }
  },

  showEventsOfDay: function(e) {
    var date = $(e.target).data('date');

    e.preventDefault();

    this.trigger('filterDate', date);
  },

  slide: function(direction, html) {
    var $html = $(html);

    this.$destination = $html.find('.js-content');
    this.$origin = this.$content;

    this.$destination.insertAfter(this.$origin);
    this.destinationHeight = this.$destination.height();

    this.$destination.addClass('sliding destination ' + direction);
    this.$origin.addClass('sliding origin ' + direction);
    this.$wrapper.addClass('sliding');
    this.$wrapper.css('height', this.destinationHeight);

    this.isSliding = true;

    this.$nav.replaceWith($html);
    this.updateNavProperties();

    this.$destination.one('webkitAnimationEnd animationend oAnimationEnd', this.onSlideEnd.bind(this));
  },

  onSlideEnd: function() {
    this.$destination.removeClass('sliding forward backward destination origin');
    this.$origin.remove();
    this.$content = this.$destination;
    this.$wrapper.removeAttr('style');
    this.$wrapper.removeClass('sliding');
    this.initEventViews();
    this.isSliding = false;
  },

  updateNavProperties: function() {
    this.$nav = this.$('.js-cal-nav');
    this.$prev = this.$('.js-prev');
    this.$next = this.$('.js-next');
    this.$title = this.$('.js-title');
  },

  initEventViews: function() {
    this.$events = this.$('.js-event');
    $.each(this.$events, function(i, el) {
      var view = new CalendarEventView({ el: el });
    });
  },

  update: function(filters) {
    var current_year = this.$title.data('year');
    var current_month = this.$title.data('month');

    this.filters = filters;
    this.getMonth(current_year, current_month).done(function(html) {
      this.$el.html(html);
      this.$wrapper = this.$('.js-wrapper');
      this.$content = this.$('.js-content');
      this.updateNavProperties();
      this.initEventViews();
    }.bind(this));
  },

  show: function() {
    this.$el.removeClass('hidden');
  },

  hide: function() {
    this.$el.addClass('hidden');
  }
});

module.exports = CalendarView;