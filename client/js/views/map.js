var $ = require('jquery');
var Backbone = require('backbone');
var mapbox = require('mapbox.js');
var enquire = require('enquire.js');

var MapView = Backbone.View.extend({
  initialize: function() {
    var token = 'mozilla-webprod.e91ef8b3';
    var map = this.map = L.mapbox.map(this.el.id, { trackResize: false });

    enquire.register("screen and (min-width: 768px)", this.setDefaultState.bind(this));
    enquire.register("screen and (max-width: 767px)", this.setMobileState.bind(this));

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
    var bounds = [[-45, -90], [45, 130]];
    this.map.fitBounds(bounds, { animate: false });
    this.map.setZoom(2);

    var windowHeight = $(window).height();
    var boundingBoxHeight = 766;
    this.map.panBy([0, (windowHeight - boundingBoxHeight) / 2], { reset: true });
  },

  setMobileState: function() {
    var bounds = [[-45, -90], [45, 130]];
    this.map.fitBounds(bounds, { animate: false });
    this.map.setZoom(0);

    this.map.panBy([0, -40], { animate: false });
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

      var unslug = feature.properties.id.replace(/-/g , " ");
      var popupContent = toTitleCase(unslug);
      marker.bindPopup(popupContent, {
        closeButton: false,
        closeOnClick: true
      });
    });

    $.getJSON('/static/mozspaces.json', function(mozSpaces) {
      map.featureLayer.setGeoJSON(mozSpaces);
      this.trigger('ready');
    }.bind(this));

    if (this.$el.hasClass('js-world')) {
      map.featureLayer.on('click', this.onMarkerClick.bind(this));
      map.featureLayer.on('mouseover', this.onMarkerMouseOver.bind(this));
      map.featureLayer.on('mouseout', this.onMarkerMouseOut.bind(this));
    }
  },

  onMarkerMouseOver: function(e) {
    if (this.isolationMode && !e.layer.selected) {
      e.layer.setOpacity(0.75);
    }
    e.layer.openPopup();
  },

  onMarkerMouseOut: function(e) {
    if (this.isolationMode && !e.layer.selected) {
      e.layer.setOpacity(0.25);
    }
    e.layer.closePopup();
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
        marker.closePopup();
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

  highlightMarker: function(id) {
    if (!this.isolationMode) {
      this.map.featureLayer.eachLayer(function(marker) {
        if (marker.feature.properties.id !== id) {
          marker.setOpacity(0.25)
        }
      });
    }
  },

  unHighlightAllMarkers: function(id) {
    if (!this.isolationMode) {
      this.map.featureLayer.eachLayer(function(marker) {
        marker.setOpacity(1);
      });
    }
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

    enquire.register("screen and (min-width: 768px)", function() {
      var offset = this.getMarkerOffset();
      this.map.panBy([offset.x, offset.y]);
    }.bind(this));
  }
});

function toTitleCase(str) {
  return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

module.exports = MapView;