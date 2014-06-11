var _ = require('underscore');

var FormModalView = require('./formmodal');

var SpaceModalView = FormModalView.extend({
  events: _.extend({}, FormModalView.prototype.events, {
    'change .js-file-input': 'showPhotoPreview'
  }),

  initialize: function(options) {
    FormModalView.prototype.initialize.call(this);

    this.$photo = this.$('.js-photo');
  },

  showPhotoPreview: function(e) {
    this.readURL(e.target);
  },

  readURL: function(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();

      reader.onload = function (e) {
        this.$photo.attr('src', e.target.result);
      }.bind(this);

      reader.readAsDataURL(input.files[0]);
    }
  }
});

module.exports = SpaceModalView;