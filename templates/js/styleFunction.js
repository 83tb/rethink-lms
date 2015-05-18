/* 
 * Copyright (C) Error: on line 4, column 33 in Templates/Licenses/license-gpl30.txt
 The string doesn't match the expected date/time format. The string to parse was: "07-May-2015". The expected format was: "MMM d, yyyy". miko
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */


var styleFunction = (function () {

	var styles = {
		bgColor: [205, 220, 1, 1],
		lineColor: [80, 192, 233, 1],
		width: 6
//		width
//		on
//		off
//		error
//		alert
// selected
	};
//	console.log('STYLING TOP feature.getProperties()');

	var colorBreath = function () {
		return [255, 255, 255, 0];
	};

	var drawStyle = function (styleSet, label) {
//		console.log('drawStyle')
		return [new ol.style.Style({
				fill: new ol.style.Fill({
					color: styleSet.bgColor //#7ed328
				}),
				stroke: new ol.style.Stroke({
					color: styleSet.lineColor, //[80, 192, 233, 1], //'#50C0E9'
					width: styleSet.width
				}),
				image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
//				anchor: [0.5, 46],
					anchorXUnits: 'fraction',
					anchorYUnits: 'pixels',
					opacity: 0.75,
					src: 'data/light-bulb-0-32x32.png',
//				src: 'data/shop.svg',
//				img: $('#SVGIcon'),
					rotation: -50,
					rotateWithView: true
				})),
				image: new ol.style.Circle({
					radius: styleSet.width * 2,
					fill: new ol.style.Fill({
						color: styleSet.bgColor
					}),
					stroke: new ol.style.Stroke({
						color: styleSet.lineColor,
						width: styleSet.width / 3
					})
				}),
				text: new ol.style.Text({
					font: '12px Calibri,sans-serif',
					text: label,
					fill: new ol.style.Fill({
						color: 'red'
					}),
					stroke: new ol.style.Stroke({
						color: 'black',
						width: 2
					})
				}),
				zIndex: Infinity
			})];
	};
//					lampBrightness
//					lampStatus
	return function (feature, resolution) {
//		console.log('STYLING feature.getProperties()')
//		console.log(feature.getProperties())
//		console.log('feature.get(actual_driver_value)');
//		console.log(feature.get('actual_driver_value'));
		var blue = 255 - feature.get('actual_driver_value');
		//[205, 220, blue, 1]
		return drawStyle(styles, feature.get('identifier'));
	};
})();

var styleFunctionS = (function () {
	return function (feature, resolution) {
		var colorBreath = function () {
			return [255, 255, 255, 0];
		};
		return [new ol.style.Style({
				fill: new ol.style.Fill({
					color: 'grey'
				}),
				stroke: new ol.style.Stroke({
					color: colorBreath(), //'red',
					width: 2
				}),
				image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
					anchor: [0.5, 46],
					anchorXUnits: 'fraction',
					anchorYUnits: 'pixels',
					opacity: 0.75,
					src: 'data/light-bulb-1-32x32.png',
//								src: 'data/shop.svg',
//								img: $('#SVGIcon'),
					rotation: 50,
					rotateWithView: true
				})),
				text: new ol.style.Text({
					font: '12px Calibri,sans-serif',
					text: feature.get('identifier'),
					fill: new ol.style.Fill({
						color: 'red'
					}),
					stroke: new ol.style.Stroke({
						color: 'black',
						width: 2
					})
				})
			})];
	};
})();