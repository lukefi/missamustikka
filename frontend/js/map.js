var WMS_BASE_LAYER = 'maastokartta';
var WMS_IMAGE_FORMAT = 'image/png';
var WMS_URL = 'http://avoindata.maanmittauslaitos.fi/mapcache/wmts/';
var berryUrl = 'http://apps3test.luke.fi:8080/geoserver/riistadb/wms';

proj4.defs("EPSG:3067",
				"+proj=utm +zone=35 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");

var laji = "mustikka";

// Check laji from url
function checkLajiParam(l) {
	if (window.location.href.search("laji=" + l) != -1) {
		laji = l;
	}
}
checkLajiParam("mustikka");
checkLajiParam("puolukka");
checkLajiParam("karpalo");
checkLajiParam("vadelma");

var map = null;
var view = null;
var projection = null;

function makeMap() {
	var mapDiv = $("#mapContainer");
	var extent = [ -548576.000000, 6291456.000000, 1548576.000000,
			8388608.000000 ];
	var center = [ 372013.0, 6674422.0 ];
	projection = ol.proj.get('EPSG:3067');
	var resolutions = [ 2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1, 0.5,
			0.25 ];
	var tileGrid = new ol.tilegrid.WMTS({
		extent : extent,
		resolutions : resolutions,
		matrixIds : [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]
	});
	var tileSource = new ol.source.WMTS({
		url : WMS_URL,
		format : WMS_IMAGE_FORMAT,
		layer : WMS_BASE_LAYER,
		matrixSet : 'ETRS-TM35FIN',
		tileGrid : tileGrid,
		attributions : [ "Taustakartat © MML" ]
	});
	var tileLayer = new ol.layer.Tile({
		extent : extent,
		source : tileSource,
		opacity : 0.8
	});
	var berrySource = new ol.source.TileWMS({
		url : berryUrl,
		params : {
			'LAYERS' : 'riistadb:' + laji,
			'TILED' : true
		},
		servertype : 'geoserver',
		tileGrid : tileGrid
	});
	var berryLayer = new ol.layer.Tile({
		source : berrySource,
		visible : true,
		opacity : 0.9
	});
	view = new ol.View({
		projection : projection,
		resolutions : resolutions,
		extent : extent,
		center : center,
		zoom : 10
	});
	map = new ol.Map({
		target : "mapContainer",
		view : view,
		controls : ol.control.defaults(),
		logo : null
	});

	// Add layers
	map.addLayer(tileLayer);
	map.addLayer(berryLayer);

	mapDiv.data('map', map);
	userLocation();
}

function userLocation() {
	// geolocation.bindTo('projection', view);
	if ("geolocation" in navigator) {
		var button = $("#userLocationBtn");
		var geolocation = new ol.Geolocation({
			projection : projection,
			tracking : true
		});
		button.click(function() {
			map.getView().setCenter(geolocation.getPosition());
		});
	}
}

$(document).ready(function() {
	// Generate map
	makeMap();

	// Init tooltip
	$('[data-toggle="tooltip"]').tooltip();

	// Update laji text to header
	$("#lajiInfoTxt").text(laji);
});
