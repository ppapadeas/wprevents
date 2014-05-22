var $ = require('jquery');
var Backbone = require('backbone');
var mapbox = require('mapbox.js');

var MapView = Backbone.View.extend({
  initialize: function() {
    var map = L.mapbox.map('map', 'examples.map-i86nkdio');

    map.setView([40, -74.50], 9);
  }
});

module.exports = MapView;