var $ = require('jquery');
var Backbone = require('backbone');

Backbone.$ = $;

var EventModalView = require('./views/eventmodal');
var DedupeModalView = require('./views/dedupemodal');

$(function() {

  // 'New event' button
  $('.js-new-event').on('click', function(e) {
    e.preventDefault();

    var modal = new EventModalView({ url: $(this).attr('href') });
  });

  // 'Edit' action
  $('.js-edit-event').on('click', function(e) {
    e.preventDefault();

    var modal = new EventModalView({ url: $(this).attr('href') });
  });

  // 'Dedupe' action
  $('.js-dedupe-event').on('click', function(e) {
    // e.preventDefault();

    var modal = new DedupeModalView({ url: $(this).attr('href') });
  });

});