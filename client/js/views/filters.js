var _ = require('underscore');
var Backbone = require('backbone');

var FiltersView = Backbone.View.extend({
  events: {
    "change #space-filter": "spaceChanged",
    "change #area-filter": "areaChanged",
    "keyup #keyword-filter": "lazyKeywordChanged",

    "keydown #keyword-filter": "preventSubmitOnEnter",
    "keydown #start-date-filter": "preventSubmitOnEnter",
    "keydown #end-date-filter": "preventSubmitOnEnter",
  },

  initialize: function() {
    this.$filters = this.$('.js-filter');
  },

  spaceChanged: function() {
    this.refresh();
  },

  areaChanged: function() {
    this.refresh();
  },

  preventSubmitOnEnter: function(e) {
    if(e.keyCode == 13) {
      e.preventDefault();
      return false;
    }
  },

  lazyKeywordChanged: _.debounce(function() {
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
  },

  refresh: function() {
    this.trigger('change', this.getCurrentFilters());
  }
});

module.exports = FiltersView;
