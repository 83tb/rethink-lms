/* 
 * Copyright (C) Error: on line 4, column 33 in Templates/Licenses/license-wp-gpl20.txt
 The string doesn't match the expected date/time format. The string to parse was: "25-May-2015". The expected format was: "MMM d, yyyy". miko
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */

//	Not used ae the moment
//			$scope.defaults {
//				events: {
//					map: [
//						'singleclick',
//						'pointermove'
//					],
//					layers: [
//						'mousemove',
//						'click'
//					]
//				},
//			}

//		$scope.$on('openlayers.map.singleclick', function (event, data) {
//			var prj = ol.proj.transform([data.coord[0], data.coord[1]], data.projection, 'EPSG:4326').map(function (c) {
//				return c.toFixed(8);
//			});
//			console.log('[' + prj + ']');
//		});
//		$scope.$on('openlayers.layers.lampsLayer.click', function (event, feature) {
//			console.log('lampsLayer.click');
////						$scope.$apply(function (scope) {
////							if (feature) {
////								console.log(feature.getProperties());
////								feature.setStyle(olHelpers.createStyle({
////									fill: {
////										color: '#FFF'
////									}
////								}));
////							}
////						});
//		});
