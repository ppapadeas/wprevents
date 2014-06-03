var _ = require('underscore');

var FormModalView = require('./formmodal');
var ColorPickerView = require('./colorpicker');

var AreaModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {

  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    var colorpicker = new ColorPickerView({ el: '.js-color-picker' });
  },

  initColorPicker: function() {

  }
});

module.exports = AreaModalView;