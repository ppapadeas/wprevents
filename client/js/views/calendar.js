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

    this.isSliding = false;

    this.initEventViews();
  },

  getNextMonth: function() {
    return this.$content.clone();
  },

  onClickNext: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.slide('forward');
    }
  },

  onClickPrev: function(e) {
    e.preventDefault();

    if (!this.isSliding) {
      this.slide('backward');
    }
  },

  slide: function(direction) {
    this.$destination = this.getNextMonth();
    this.$origin = this.$content;

    this.$destination.insertAfter(this.$origin);
    this.destinationHeight = this.$destination.height();

    this.$destination.addClass('destination ' + direction);
    this.$origin.addClass('origin ' + direction);
    this.$wrapper.css('height', this.destinationHeight + 20); // 20px padding

    this.isSliding = true;

    setTimeout(function() {
      this.onSlideEnd();
    }.bind(this), 1);
  },

  onSlideEnd: function() {
    this.$destination.addClass('sliding');
    this.$origin.addClass('sliding');

    var fakeData = { previousMonth: 'May 2014', nextMonth: 'July 2014', currentMonth: 'June 2014' };
    this.updateHeader(fakeData);

    this.$destination.one('webkitTransitionEnd transitionend oTransitionEnd', function() {
      this.$destination.removeClass('sliding forward backward destination origin');
      this.$origin.remove();
      this.$content = this.$destination;
      this.$wrapper.removeAttr('style');
      this.initEventViews();
      this.isSliding = false;
    }.bind(this));
  },

  updateHeader: function(data) {
    this.$prev.find('span').text(data.previousMonth);
    this.$next.find('span').text(data.nextMonth);
    this.$title.text(data.currentMonth);
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