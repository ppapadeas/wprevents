var $ = require('jquery');
var jQueryForm = require('jquery-form/jquery.form');
var Backbone = require('backbone');

Backbone.$ = $;

var ModalContainerView = require('./views/modalcontainer');
var EventModalView = require('./views/eventmodal');
var DedupeModalView = require('./views/dedupemodal');

$(function() {
  var container = new ModalContainerView({ el: $('.modal-container') });

  // 'New event' button
  $('.js-new-event').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(EventModalView, path);

    e.preventDefault();
  });

  // 'Edit' action
  $('.js-edit-event').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(EventModalView, path);

    e.preventDefault();
  });

  // 'Dedupe' action
  $('.js-dedupe-event').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(DedupeModalView, path);

    e.preventDefault();
  });

});