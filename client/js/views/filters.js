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
    "keydown #start-date-filter": "preventSubmitOnEnter",
    "keydown #end-date-filter": "preventSubmitOnEnter",
  },

  initialize: function() {
    this.$filters = this.$('.js-filter');

    this.$('.js-datepicker').each(function() {
      new Pikaday({ field: this });
    });
  },

  preventSubmitOnEnter: function(e) {
    if(e.keyCode == 13) {
      e.preventDefault();
      return false;
    }
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
