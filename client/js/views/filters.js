var _ = require('underscore');
var Backbone = require('backbone');
var Pikaday = require('pikaday');

var FiltersView = Backbone.View.extend({
  events: {
    "change #space-filter": "refresh",
    "change #area-filter": "refresh",
    "keyup #keyword-filter": "lazyRefresh",
    "change #start-date-filter": "refresh",
    "change #end-date-filter": "refresh",

    "keydown #keyword-filter": "preventSubmitOnEnter",
    "keydown #start-date-filter": "onDateKeydown",
    "keydown #end-date-filter": "onDateKeydown",
  },

  initialize: function() {
    this.$filters = this.$('.js-filter');

    this.$('.js-datepicker').each(function() {
      new Pikaday({ field: this });
    });
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

  onDateKeydown: function(e) {
    this.preventSubmitOnEnter(e);
    this.clearOnBackspace(e);
  },

  refresh: function() {
    this.trigger('change', this.getCurrentFilters());
  },

  lazyRefresh: _.debounce(function() {
    this.refresh();
  }, 400),

  getCurrentFilters: function() {
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

    return filters;
  }
});

module.exports = FiltersView;
