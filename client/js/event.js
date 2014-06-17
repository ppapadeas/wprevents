var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');

var MapView = require('./views/map');

Backbone.$ = $;

var map = new MapView({ el: '#map' });
var spaceId = $('.js-event-space').data('space');

map.on('ready', function() {
  map.focusSpace(spaceId);
});