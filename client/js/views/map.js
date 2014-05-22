var $ = require('jquery');
var Backbone = require('backbone');
var mapbox = require('mapbox.js');

var MapView = Backbone.View.extend({
  initialize: function() {
    var map = L.mapbox.map('map', 'wavecaller.iacp9hm4');
  }
});

module.exports = MapView;