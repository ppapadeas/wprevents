var $ = require('jquery');
var Backbone = require('backbone');
var mapbox = require('mapbox.js');

var MapView = Backbone.View.extend({
  initialize: function() {
    var token = 'mozilla-webprod.e91ef8b3';
    var map = this.map = L.mapbox.map(this.el.id);

    this.setDefaultState();

    this.isolationMode = false;

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

  setDefaultState: function() {
    // Bounds order is [South West, North East]
    var bounds = [[-45, -130], [45, 130]];
    this.map.fitBounds(bounds);
    this.map.setZoom(2);

    var windowHeight = $(window).height();
    var boundingBoxHeight = 766;
    this.map.panBy([0, (windowHeight - boundingBoxHeight) / 2], {
      animate: false
    });
  },

  /*
   * Creates spaces markers and then hide them using setFilter()
   */
  initSpacesMarkers: function () {
    var map = this.map;

    map.featureLayer.on('layeradd', function(e) {
      var marker = e.layer,
          feature = marker.feature;

      marker.setIcon(L.icon(feature.properties.icon));
      marker.selected = false;
    });

    $.getJSON('/static/mozspaces.json', function(mozSpaces) {
      map.featureLayer.setGeoJSON(mozSpaces);
      this.trigger('ready');
    }.bind(this));

    map.featureLayer.on('click', this.onMarkerClick.bind(this));
    map.featureLayer.on('mouseover', this.onMarkerMouseOver.bind(this));
    map.featureLayer.on('mouseout', this.onMarkerMouseOut.bind(this));
  },

  onMarkerMouseOver: function(e) {
    if (this.isolationMode && !e.layer.selected) {
      e.layer.setOpacity(0.75);
    }
  },

  onMarkerMouseOut: function(e) {
    if (this.isolationMode && !e.layer.selected) {
      e.layer.setOpacity(0.25);
    }
  },

  onMarkerClick: function(e) {
    this.map.featureLayer.eachLayer(function (marker) {
      if (marker !== e.layer) {
        marker.setOpacity(0.25);
        marker.selected = false;
      } else {
        marker.setOpacity(1);
        marker.selected = true;
      }
    });

    var markerId = e.layer.feature.properties.id;
    this.trigger('markerClick', markerId);
  },

  doClickMarker: function(marker) {
    marker.fireEvent('click');
  },

  selectMarker: function(id) {
    this.map.featureLayer.eachLayer(function(marker) {
      if (marker.feature.properties.id === id) {
        this.doClickMarker(marker);
      }
    }.bind(this));

    this.isolationMode = true;
  },

  deselectMarker: function() {
    this.map.featureLayer.eachLayer(function(marker) {
      marker.setOpacity(1);
      marker.selected = false;
    });

    this.isolationMode = false;
  },

  hideSpacesMarkers: function() {
    this.map.featureLayer.setFilter(function () {
      return false;
    });
  },

  getMarkerOffset: function() {
    var offset = {};
    var tabletBreakPoint = 1010;
    var tabletMode = $(window).width() > tabletBreakPoint ? true : false;
    var pageWidth =  tabletMode ? 980 : 740;
    var markerHeight = 45;
    var rightMargin = tabletMode ? 80 : 60;
    var topMargin = 20;
    var headerOffset = $('.js-event-header').offset().top;
    offset.x = - (pageWidth / 2) + rightMargin;
    offset.y = (($(window).height() - ((headerOffset + markerHeight) * 2)) / 2) - topMargin;

    return offset;
  },

  focusSpace: function(id) {
    this.map.featureLayer.eachLayer(function (marker) {
      if (marker.feature.properties.id === id) {
        var markerCoords = this.markerCoords = marker.getLatLng();
        this.map.setView(markerCoords, 10, {
          animate: true
        });
      }
    }.bind(this));

    var offset = this.getMarkerOffset();
    this.map.panBy([offset.x, offset.y]);
  }
});

module.exports = MapView;