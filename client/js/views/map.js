var $ = require('jquery');
var Backbone = require('backbone');
var mapbox = require('mapbox.js');

var MapView = Backbone.View.extend({
  initialize: function() {
    var token = 'mozilla-webprod.e91ef8b3';
    var map = this.map = L.mapbox.map(this.el.id);//.setView([0, 0], 2);
    // Bounds order is [South West, North East]
    var bounds = [[-45, -130], [45, 130]];
    map.fitBounds(bounds);
    map.setZoom(2);

    var windowHeight = $(window).height();
    var boundingBoxHeight = 766;
    map.panBy([0, (windowHeight - boundingBoxHeight) / 2]);

    var mapLayer = L.mapbox.tileLayer(token,{
        detectRetina: true
    });

    // when ready, set the map and page default states
    mapLayer.on('ready', function () {
      // touch support detection.
      var touch = L.Browser.touch || L.Browser.msTouch;
      // add tile layer to the map
      mapLayer.addTo(map);
      // disable map zoom on scroll.
      map.scrollWheelZoom.disable();
      // create spaces markers.
      this.initSpacesMarkers();

      // disable dragging for touch devices.
      if (touch) {
        // disable drag and zoom handlers.
        map.dragging.disable();
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        // disable tap handler, if present.
        if (map.tap) {
          map.tap.disable();
        }
      }
    }.bind(this));
  },

  /*
   * Creates spaces markers and then hide them using setFilter()
   */
  initSpacesMarkers: function () {
    var map = this.map;

    map.markerLayer.on('layeradd', function(e) {
      var marker = e.layer,
          feature = marker.feature;

      marker.setIcon(L.icon(feature.properties.icon));
    });

    $.getJSON('/static/mozspaces.json', function(mozSpaces) {
      map.markerLayer.setGeoJSON(mozSpaces);
    });
  },

  hideSpacesMarkers: function() {
    this.map.markerLayer.setFilter(function () {
      return false;
    });
  }
});

module.exports = MapView;