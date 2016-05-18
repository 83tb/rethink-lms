/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */


var controlLocate = function(opt_options) {

    var options = opt_options || {};
    var location = 0;

    var button = document.createElement('button');
    //	button.innerHTML = 'N';
    button.className = "icon geolocate fa fa-location-arrow";

    var this_ = this;
    var handleRotateNorth = function(e) {
        rotation += 90;
        this_.getMap().getView().setRotation(rotation);
    };

    button.addEventListener('click', handleRotateNorth, false);
    button.addEventListener('touchstart', handleRotateNorth, false);

    var element = document.createElement('div');
    element.className = 'ol-control-location ol-unselectable ol-control';
    element.appendChild(button);

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });
};
ol.inherits(controlLocate, ol.control.Control);


var controlOverview = new ol.control.OverviewMap({
    // see in overviewmap-custom.html to see the custom CSS used
    className: 'ol-overviewmap ol-custom-overviewmap',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.TileJSON({
                projection: 'EPSG:3857',
                url: '//api.tiles.mapbox.com/v3/stndev.idlelalf.jsonp'
            })
        })
    ],
    collapseLabel: '\u00BB',
    label: '\u00AB',
    collapsed: true
});
