var Backbone = require('backbone');
var CalendarEventView = require('./calendarevent');

var CalendarView = Backbone.View.extend({
  events: {
    'click .js-prev': 'onClickPrev',
    'click .js-next': 'onClickNext'
  },

  initialize: function() {
    this.$prev = this.$('.js-prev');
    this.$next = this.$('.js-next');
    this.$title = this.$('.js-title');
    this.$wrapper = this.$('.js-wrapper');
    this.$content = this.$('.js-content');
    this.$nav = this.$('.js-cal-nav');

    this.isSliding = false;

    this.initEventViews();
  },

  getMonth: function(year, month) {
    return $.get('/calendar_month?' + $.param({
      year: year,
      month: month
    }));
  },

  getNextMonth: function() {
    return this.getMonth(this.$next.data('year'), this.$next.data('month'));
  },

  getPreviousMonth: function() {
    return this.getMonth(this.$prev.data('year'), this.$prev.data('month'));
  },

  onClickNext: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.getNextMonth().done(function(html) {
        this.slide('forward', html);
      }.bind(this));
    }
  },

  onClickPrev: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.getPreviousMonth().done(function(html) {
        this.slide('backward', html);
      }.bind(this));
    }
  },

  slide: function(direction, html) {
    var $html = $(html);

    this.$destination = $html.find('.js-content');
    this.$origin = this.$content;

    this.$destination.insertAfter(this.$origin);
    this.destinationHeight = this.$destination.height();

    this.$destination.addClass('destination ' + direction);
    this.$origin.addClass('origin ' + direction);
    this.$wrapper.css('height', this.destinationHeight);

    this.isSliding = true;

    this.updateNav($html);

    setTimeout(function() {
      this.onSlideEnd();
    }.bind(this), 1);
  },

  onSlideEnd: function() {
    this.$destination.addClass('sliding');
    this.$origin.addClass('sliding');

    this.$destination.one('webkitTransitionEnd transitionend oTransitionEnd', function() {
      this.$destination.removeClass('sliding forward backward destination origin');
      this.$origin.remove();
      this.$content = this.$destination;
      this.$wrapper.removeAttr('style');
      this.initEventViews();
      this.isSliding = false;
    }.bind(this));
  },

  updateNav: function($html) {
    var $newNav = $html.find('.js-cal-nav');

    this.$nav.replaceWith($newNav);
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
    console.log("Filtering event list with:", filters);

    // TODO: XHR to update event list
  }
});

module.exports = CalendarView;