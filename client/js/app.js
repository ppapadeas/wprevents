var $ = require('jquery');
var Backbone = require('backbone');

Backbone.$ = $;

var MapView = require('./views/map');


var App = function() {
  var map = new MapView();
}

$(function() {
  var app = new App();
});