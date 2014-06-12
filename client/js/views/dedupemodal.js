var _ = require('underscore');

var ModalView = require('./modal');


var DedupeModalView = ModalView.extend({
  events: _.extend({}, ModalView.prototype.events, {
    'click .js-delete': 'deleteDuplicateEvent',
    'keyup .js-name-filter': 'filterByName'
  }),

  initialize: function(options) {
    ModalView.prototype.initialize.call(this);

    this.token = $("input[name='csrfmiddlewaretoken']").val();
  },

  deleteDuplicateEvent: function(e) {
    var $row = $(e.target).closest('tr');
    var id = $row.data('id');

    e.preventDefault();

    $.ajax({
      url: "/admin/events/ajax_delete",
      data: {
        id: id
      },
      type: "POST",
      beforeSend: function (request) {
        request.setRequestHeader("X-CSRFToken", this.token);
      }.bind(this),
      success: function(response) {
        // Don't check whether the status is successful or not.
        // If the event was already removed by another user,
        // fail silently and remove the line anyway.
        $.when($row.fadeOut()).done(function() {
          $row.remove();
          this.trigger('deleteEvent', id);
        }.bind(this));
      }.bind(this)
    });
  },

  filterByName: function(e) {
    var keyword = e.target.value;
    var $rows = this.$('tbody tr');

    $rows.each(function() {
      var $row = $(this);
      var name = $row.children(':first').html();

      $row.removeClass('hidden');
      if (name.indexOf(keyword) == -1) {
        $row.addClass('hidden');
      }
    });
  }
});

module.exports = DedupeModalView;