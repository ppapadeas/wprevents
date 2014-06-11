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
    "change select": "blur",

    "keydown #keyword-filter": "preventSubmitOnEnter",
    "keydown #start-date-filter": "onDateKeydown",
    "keydown #end-date-filter": "onDateKeydown",
  },

  initialize: function() {
    this.currentFilters = {};

    this.$filters = this.$('.js-filter');
    this.$spaceFilter = this.$('.js-space-filter');
    this.$dateFilters = this.$('.js-datepicker');

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

  blur: function(e) {
    $(e.target).blur();
  },

  onDateKeydown: function(e) {
    this.preventSubmitOnEnter(e);
    this.clearOnBackspace(e);
  },

  lazyRefresh: _.debounce(function() {
    this.refresh();
  }, 400),

  setSpace: function(id) {
    var isFound = false;

    // check if id exists
    this.$spaceFilter.find('option').each(function() {
      if ($(this).attr('value') === id) {
        isFound = true;
      }
    });

    if (isFound) {
      this.$spaceFilter.val(id);
      this.refresh();
    } else {
      console.error('Filter value was not found:', id);
    }
  },

  setDates: function(date) {
    this.$dateFilters.val(date);
  },

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
        $(this).addClass('active');
        filters[this.name] = value;
      } else {
        $(this).removeClass('active');
      }
    });

    if (!_.isEqual(filters, this.currentFilters)) {
      this.currentFilters = filters;
      this.trigger('change', filters);
    }
  },

  enableDateFilters: function() {
    this.$dateFilters.prop('disabled', false);
  },

  disableDateFilters: function() {
    this.$dateFilters.prop('disabled', true);
  }
});

module.exports = FiltersView;
