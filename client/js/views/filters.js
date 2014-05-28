var _ = require('underscore');
var Backbone = require('backbone');
var Pikaday = require('pikaday');

var FiltersView = Backbone.View.extend({
  events: {
    "change #space-filter": "refresh",
    "change #area-filter": "refresh",
    "keyup #keyword-filter": "lazyRefresh",
    "change #end-date-filter": "refresh",

    "keydown #keyword-filter": "preventSubmitOnEnter",
    "keydown #start-date-filter": "onDateKeydown",
    "change #start-date-filter": "onStartDateChange",
    "keydown #end-date-filter": "onDateKeydown",
  },

  initialize: function() {
    this.currentFilters = {};

    this.$filters = this.$('.js-filter');

    this.datePickers = [];

    this.$('.js-datepicker').each(function(i, el) {
      var picker = new Pikaday({ field: el });
      this.datePickers.push(picker);
    }.bind(this));

    this.startDate = this.datePickers[0];
    this.endDate = this.datePickers[1];
  },

  preventSubmitOnEnter: function(e) {
    if (e.keyCode == 13) { // Enter key
      e.preventDefault();
      return false;
    }
  },

  clearOnBackspace: function(e) {
    if (e.keyCode == 8) { // Backspace key
      $(e.target).val('').blur();
      this.refresh();
    }
  },

  onStartDateChange: function(e) {
    var date = this.startDate.getDate();

    // set end date to start date
    // only if end date hasn't yet been set
    if (this.endDate.getDate() === null) {
      this.endDate.setDate(date);
    }

    this.refresh();
  },

  onDateKeydown: function(e) {
    this.preventSubmitOnEnter(e);
    this.clearOnBackspace(e);
  },

  lazyRefresh: _.debounce(function() {
    this.refresh();
  }, 400),

  refresh: function() {
    var filters = {};

    this.$filters.each(function() {
      var value;

      if (this.type === 'select-one') {
        value = this.options[this.selectedIndex].value;
      } else if (this.type === 'text') {
        value = this.value;
      }

      if (value && value !== '') {
        filters[this.name] = value;
      }
    });

    if (!_.isEqual(filters, this.currentFilters)) {
      this.currentFilters = filters;
      this.trigger('change', filters);
    }
  }
});

module.exports = FiltersView;
