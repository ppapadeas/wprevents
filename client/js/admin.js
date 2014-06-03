var $ = require('jquery');
var jQueryForm = require('jquery-form/jquery.form');
var Backbone = require('backbone');

Backbone.$ = $;

var ModalContainerView = require('./views/modalcontainer');
var EventModalView = require('./views/eventmodal');
var DedupeModalView = require('./views/dedupemodal');
var SpaceModalView = require('./views/spacemodal');
var AreaModalView = require('./views/areamodal');

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

  // 'New space' button
  $('.js-new-space').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(SpaceModalView, path);

    e.preventDefault();
  });

  // 'Edit space' action
  $('.js-edit-space').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(SpaceModalView, path);

    e.preventDefault();
  });

  // 'New area' button
  $('.js-new-area').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(AreaModalView, path);

    e.preventDefault();
  });

  // 'Edit area' action
  $('.js-edit-area').on('click', function(e) {
    var path = $(this).attr('href');
    var modal = container.setCurrentModal(AreaModalView, path);

    e.preventDefault();
  });

});