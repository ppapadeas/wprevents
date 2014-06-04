var _ = require('underscore');
var Backbone = require('backbone');

var TabsView = Backbone.View.extend({
  events: {
    'click .js-list-tab': 'clickListTab',
    'click .js-calendar-tab': 'clickCalendarTab'
  },

  initialize: function() {
    this.tabs = {
      list: this.$('.js-list-tab'),
      calendar: this.$('.js-calendar-tab')
    };
  },

  clickListTab: function(e) {
    e.preventDefault();

    if (!$(this).hasClass('active')) {
      this.trigger('navigate', '');
    }
  },

  clickCalendarTab: function(e) {
    e.preventDefault();

    if (!$(this).hasClass('active')) {
      this.trigger('navigate', 'calendar');
    }
  },

  activate: function(id) {
    if (!_.has(this.tabs, id)) return;

    _.each(this.tabs, function(tab) {
      tab.removeClass('active');
    });

    this.tabs[id].addClass('active');
  }
});

module.exports = TabsView;