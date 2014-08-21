var _ = require('underscore');
var Pikaday = require('pikaday');

var FormModalView = require('./formmodal');
var AreaSelectView = require('./areaselect');


var EventModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {
    'change #id_space': 'onChangeSpace'
  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    this.areaSelect = new AreaSelectView({ el: $('.js-area-select') });
    this.$('.js-datepicker').each(function() {
      new Pikaday({ field: this });
    });

    this.$space = this.$('#id_space');
    this.$startDate = this.$('.js-start-date');
    this.$startTime = this.$('.js-start-time');
    this.$endDate = this.$('.js-end-date');
    this.$endTime = this.$('.js-end-time');

    this.currentSpace = this.$space.val();
    this.isNewEvent = this.$el.hasClass('js-new-event');
  },

  // Each time a space is selected, we convert dates and times
  // according to the timezone of the chosen space
  onChangeSpace: function() {
    // Don't convert dates and times for new events
    if (this.isNewEvent) return;

    var values = {
      current_space: this.currentSpace,
      new_space: this.$space.val(),
      start_date: this.$startDate.val(),
      start_time: this.$startTime.val(),
      end_date: this.$endDate.val(),
      end_time: this.$endTime.val()
    };

    // If any of the date/time fields is empty, don't convert
    if (!values.start_date || !values.start_time || !values.end_date || !values.end_time) {
      return;
    }

    $.ajax({
      url: '/admin/events/convert?' + $.param(values),
      type: 'GET'
    }).done(function(data) {
      this.$startDate.val(data.start_date);
      this.$startTime.val(data.start_time);
      this.$endDate.val(data.end_date);
      this.$endTime.val(data.end_time);
    }.bind(this));

    this.currentSpace = values.new_space;
  }
});

module.exports = EventModalView;