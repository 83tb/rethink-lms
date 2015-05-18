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

var app = angular.module('lmsUI', ['openlayers-directive']);

app.controller('lmsController', ['$scope', '$location', '$timeout', '$http', 'olData', 'olHelpers', 'adjsServis',
	function ($scope, $location, $timeout, $http, olData, olHelpers, adjsServis) {
//		$scope.adjustments = adjsServis;

		angular.extend($scope, {
			appHelpers: {
				isValidBounds: function (bounds) {
					return angular.isDefined(bounds) && (
									(angular.isArray(bounds) && bounds.length === 4 &&
													angular.isNumber(bounds[0]) && angular.isNumber(bounds[1]) &&
													angular.isNumber(bounds[1]) && angular.isNumber(bounds[2])) ||
									(angular.isArray(bounds) && bounds.length === 4 &&
													angular.isArray(bounds[0]) && bounds[0].length === 2 && angular.isNumber(bounds[0][0]) && angular.isNumber(bounds[0][1]) &&
													angular.isArray(bounds[1]) && bounds[1].length === 2 && angular.isNumber(bounds[1][0]) && angular.isNumber(bounds[1][1]) &&
													angular.isArray(bounds[2]) && bounds[2].length === 2 && angular.isNumber(bounds[2][0]) && angular.isNumber(bounds[2][1]) &&
													angular.isArray(bounds[3]) && bounds[3].length === 2 && angular.isNumber(bounds[3][0]) && angular.isNumber(bounds[3][1])
													&& bounds[3][1] > 1
													)
									);
				},
				isResponse: function (resp) {
					return angular.isDefined(resp.response) &&
									(angular.isArray(resp.response) &&
													resp.response.length > 0);
				},
				isProperData: function (data) {
					return angular.isDefined(data) &&
									(angular.isArray(data) &&
													data.length > 0);
				},
			}
		});

		angular.extend($scope, {
			fStyle: styleFunction,
			selectStyle: styleFunctionS,
			changesLog: {
				lampStatus: 0,
				lampBrightness: 0
			},
			view: {
				rotation: 0
			},
			degrees: 0,
			defaults: {
				layers: {
					main: {
						name: 'MapboxDefault',
						source: {
							type: 'TileJSON',
							url: 'http://api.tiles.mapbox.com/v3/stndev.idlelalf.jsonp'
						}
					}
				},
				controls: {
					attribution: false,
					rotate: {
						name: "rotate",
						active: true,
						autoHide: false
					},
					zoom: true,
//								fullscreen: true,
//								mousePosition: true,
//								OverviewMap: true
//								ScaleLine
//								ZoomSlider
//								ZoomToExtent
				},
				interactions: {
					mouseWheelZoom: true,
					doubleClickZoom: false
//								select: //true
//									selectFn
				},
				view: {
					maxZoom: 24,
					minZoom: 10,
					rotation: 0
				},
				events: {
					map: [
						'singleclick',
						'pointermove'
					],
					layers: [
						'mousemove',
						'click'
					]
				}
			},
			offset: 0,
			center: {
				lat: 0,
				lon: 0,
				bounds: [],
				zoom: 20,
				autodiscover: true,
				centerUrlHash: true,
				rotation: 0,
				windowBounds: []
			},
			layers: [],
			changeLayer: function (layer) {
				$scope.layers.map(function (l) {
					console.log(layer.active);
					l.active = (l === layer);
				});
			},
			lampsLayer: {},
			markers: []
		});
		$scope.markers = []
//			{
//							stn: {
//								name: 'stn',
//								lat: 52.175248828722204,
//								lon: 20.815872371653256,
//								label: {
//									message: 'loading...',
//									show: true,
//									showOnMouseOver: true
//								},
//								style: {
//									image: {
//										icon: {
//											anchor: [0, 0], //[0.5, 1],
//											anchorXUnits: 'fraction',
//											anchorYUnits: 'fraction',
//											opacity: 0.90,
//											src: 'data/priority-high.png'
//										}
//									}
//								}
//							}
//		};


		$scope.setLampsLayer = function (data) {
			// we don't need this any more(?)
			$scope.lData = data;
			console.log('setLampsLayer $scope.lData');
			console.log($scope.lData);
			// not used anyware

			if (!$scope.appHelpers.isResponse(data))
				return;

			//
			// get source get features if they exist
			//
			//
			$scope.lampsSrc = {
				type: "FeatureCollection",
				features: []
			};
			angular.forEach(data.response, function (lamp) {
				var feature = {
					id: lamp.id,
					name: lamp.identifier,
					type: "Feature",
					geometry: {
						type: lamp.location.type,
						coordinates: lamp.location.coordinates
					},
					properties: {
						identifier: lamp.identifier,
						//
						// Gropus - combine lamps (extents + margin) with same group id
						//  -> create poligon 
						//  -> add to groups Layer as a feature!!!
						//
						group: lamp.group,
						//
						working_l_setting: lamp.working_l_setting,
						special_l_setting: lamp.special_l_setting,
						presence_l_setting: lamp.presence_l_setting,
						wanted_l_level: lamp.wanted_l_level,
						actual_driver_value: lamp.actual_driver_value,
						presence_flag: lamp.presence_flag,
						special_flag: lamp.special_flag,
						working_flag: lamp.working_flag,
						change_required: lamp.change_required
					}
				};
				$scope.lampsSrc.features.push(feature);
			});
//			.then(function () {
			console.log('then: $scope.lampsSrc');
			console.log($scope.lampsSrc);

			$scope.lampsLayer = {
//							clustering: true, 
//							clusteringDistance: 40,
				name: 'lampsLayer',
				source: {
					type: 'GeoJSON',
					geojson: {
						object: $scope.lampsSrc,
						projection: 'EPSG:3857'
					}
				},
				style: $scope.fStyle
			};
//			});
		};

		$scope.setExt = function () {
			olData.getMap().then(function (map) {
				var extent = [[20.63249140, 52.12195456], [20.61395197, 52.13565408], [20.67540675, 52.15482633], [20.69772272, 52.13691844]];
				var toExtent = ol.extent.applyTransform([extent[1][0], extent[1][1], extent[3][0], extent[3][1]], ol.proj.getTransform("EPSG:4326", "EPSG:3857"));
				map.getView().fitExtent(toExtent, map.getSize());
			});
		}

		$scope.$on("centerUrlHash", function (event, centerHash) {
			//set from url&r=rotation =>  Math.PI / rotation
			var rotation = $location.search().r
			if (rotation) {
				$scope.view.rotation = rotation * Math.PI / 180;
			}
			$location.search({c: centerHash});
//			console.log($scope.center);
			olData.getMap().then(function (map) {
				curextent = map.getView().calculateExtent(map.getSize());
				$scope.curextent = ol.extent.applyTransform(curextent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
			});
		});

		$scope.$watch("center.zoom", function (zoom) {
			$scope.layers.map(function (l) {
				if (l.name === 'lampsLayer') {
					if (16 < zoom && zoom < 18) {
//						l.source.url = "./json/testLayer1.geojson";
					} else if (18 <= zoom) {
//						l.source.url = "./json/testLayer2_1.geojson";
					}
				}
			});
		});

		$scope.degreesToRadians = function () {
			$scope.view.rotation = parseFloat($scope.degrees, 10).toFixed(2) * (Math.PI / 180);
		};

		$scope.logExtent = function () {
			olData.getMap().then(function (map) {
				curextent = map.getView().calculateExtent(map.getSize());
				$scope.curextent = ol.extent.applyTransform(curextent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
			});
			$scope.setMarkers();
		}
		$scope.setMarkers = function () {
			$scope.markers = [];
			angular.forEach($scope.center.windowBounds, function (point, key) {
				var colors = ['#f05222', '#7CBA01', '#00A6F0', '#FFB901'];
				var marker = {
					name: key,
					lon: point[0],
					lat: point[1],
					label: {
						message: key.toString(), // + " Lon: " + point[0] +" Lat: " + point[1],
						show: true,
						showOnMouseOver: true
					},
					style: {
						image: {
							circle: {
								radius: 50,
								fill: new ol.style.Fill({
									color: colors[key],
									opacity: 0.6
								}),
								stroke: new ol.style.Stroke({
									color: '#ffcc00',
									opacity: 0.4
								})
							}
						}
					}
				};
//				console.log(marker);
				$scope.markers.push(marker);
			});
//			console.log('$scope.markers');
//			console.log($scope.markers);
		}

		$scope.$watch('view.rotation', function (value) {
			console.log('rotated ' + ($scope.view.rotation * 180 / Math.PI).toFixed(2));
			$scope.degrees = ($scope.view.rotation * 180 / Math.PI).toFixed(2);

			olData.getMap().then(function (map) {
				curextent = map.getView().calculateExtent(map.getSize());
				$scope.curextent = ol.extent.applyTransform(curextent, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
			});

		});

		$scope.$on('openlayers.map.singleclick', function (event, data) {
			var prj = ol.proj.transform([data.coord[0], data.coord[1]], data.projection, 'EPSG:4326').map(function (c) {
				return c.toFixed(8);
			});
			console.log('[' + prj + ']');
		});
		$scope.$on('openlayers.layers.lampsLayer.click', function (event, feature) {
			console.log('lampsLayer.click');
//						$scope.$apply(function (scope) {
//							if (feature) {
//								console.log(feature.getProperties());
//							}
//						});
		});
//					$scope.$on('openlayers.layers.lampsLayer.click', function (event, feature) {
//						$scope.$apply(function (scope) {
//							if (feature) {
//								console.log(feature.getProperties());
//								feature.setStyle(olHelpers.createStyle({
//									fill: {
//										color: '#FFF'
//									}
//								}));
//								//								$scope.mouseClickCountry = feature ? $scope.countries[feature.getId()].name : '';
//							}
//						});
//					});

		$scope.patchDataOld = function () {
			$http.get('http://10.1.2.55:8888/lamps').success(function (data) {
				console.log(data)
//							// this callback will be called asynchronously
//							// when the response is available
//							$scope.newLamps = [];
//							$scope.tldata = data.lamps;
//
//							$http.get('lampHardwareList.json').success(function (data) {
//								$scope.hdata = data;
//
//								var i = 0;
//
//								angular.forEach($scope.tldata, function (lamp, key) {
//									newLamp = {};
//									delete $scope.hdata[key].identifier;
//									delete lamp.properties.virtual_sensor;
//									angular.extend(newLamp,
//													{
//														id: "",
//														location: {
//															'$reql_type$': "GEOMETRY"
//														}
//													},
//													lamp.properties
//									);
//									newLamp.hardware = $scope.hdata[key];
//									angular.extend(newLamp.location, lamp.geometry);
//
//									$scope.newLamps.push(newLamp);
//									i++;
//
//								});
//								$scope.newLampsSet = {lamps: $scope.newLamps};
//								console.log($scope.newLampsSet);
//							});
//							var pdata = {response: []};//{}
				var pdata = [];
//							var rlamp = data.response[Math.floor((Math.random() * 6))];
				var rlamp = data.response[0];
				console.log(rlamp.identifier)
				console.log(rlamp)
				trueFalse = function () {
					return !!Math.floor(Math.random() * 2);
				};
				angular.forEach(data.response, function (rl) {
					var rdata = {
						id: rl.id,
//								group: [],
						working_l_setting: 0, //Math.floor((Math.random() * 244) + 1),
						special_l_setting: 0, //Math.floor((Math.random() * 244) + 1),
						presence_l_setting: 0, //Math.floor((Math.random() * 244) + 1),
						presence_flag: false, //trueFalse(),
						special_flag: false, //trueFalse(),
						working_flag: false, //trueFalse(),
						change_required: true
					};
//							angular.extend(rlamp, rdata);
					console.log(rdata)
					pdata.push(rdata)
//							pdata = rdata;
				});

				console.log(pdata)
//							return;
				$scope.pdata = pdata;
//							console.log(vdata);

				$http.patch('http://10.1.2.55:8888/lamps', pdata).
								success(function (data, status, headers, config) {
									// this callback will be called asynchronously
									// when the response is available
									console.log(data);
									$http.get('http://10.1.2.55:8888/lamps').success(function (data) {
										console.log(data)
									});
								}).
								error(function (data, status, headers, config) {
									// called asynchronously if an error occurs
									// or server returns response with an error status.
									console.log(data);
								});
			}).
							error(function (data, status, headers, config) {
								// called asynchronously if an error occurs
								// or server returns response with an error status.
								console.log(data);
							});
		};

		$scope.postDataFile = function () {
			$http.get('./json/lampsListOUT.json').success(function (data) {
//							// this callback will be called asynchronously
//							// when the response is available
//							$scope.newLamps = [];
//							$scope.tldata = data.lamps;
//
//							$http.get('lampHardwareList.json').success(function (data) {
//								$scope.hdata = data;
//
//								var i = 0;
//
//								angular.forEach($scope.tldata, function (lamp, key) {
//									newLamp = {};
//									delete $scope.hdata[key].identifier;
//									delete lamp.properties.virtual_sensor;
//									angular.extend(newLamp,
//													{
//														id: "",
//														location: {
//															'$reql_type$': "GEOMETRY"
//														}
//													},
//													lamp.properties
//									);
//									newLamp.hardware = $scope.hdata[key];
//									angular.extend(newLamp.location, lamp.geometry);
//
//									$scope.newLamps.push(newLamp);
//									i++;
//
//								});
//								$scope.newLampsSet = {lamps: $scope.newLamps};
//								console.log($scope.newLampsSet);
//							});
//							var pdata = {response: [{lamps: []}]};//{}
//							var rlamp = data.response[0].lamps[Math.floor((Math.random() * 6))];
//							console.log(rlamp)
//							trueFalse = function(){
//								return !!Math.floor(Math.random() * 2);
//							};
//							var rdata = {
//								group: [],
//								working_l_setting: Math.floor((Math.random() * 244) + 1),
//								special_l_setting: Math.floor((Math.random() * 244) + 1),
//								presence_l_setting: Math.floor((Math.random() * 244) + 1),
//								presence_flag: trueFalse(),
//								special_flag: true,//trueFalse(),
//								working_flag: trueFalse(),
//							};
//							angular.extend(rlamp, rdata);
//							console.log(rdata)
//							pdata.response[0].lamps.push(rlamp)
//							postLamp = {response: data.lamps};
//							postLamp = [data.lamps[0]];
				postLamp = data.lamps;
				console.log(postLamp);
//							return;



//							console.log(vdata);
				$http.post('http://10.1.2.55:8888/lamps', postLamp).
//							$http.patch('http://10.1.2.55:8888/lamps', pdata).
								success(function (data, status, headers, config) {
									// this callback will be called asynchronously
									// when the response is available
									console.log(data);
								}).
								error(function (data, status, headers, config) {
									// called asynchronously if an error occurs
									// or server returns response with an error status.
									console.log(data);
								});
			}).
							error(function (data, status, headers, config) {
								// called asynchronously if an error occurs
								// or server returns response with an error status.
								console.log(data);
							});
		};





//		$scope.centerJSON = function () {
//		$scope.$watch('changesLog', function () {
//		$scope.$watch('adjsServis', function(){
		$scope.$on('adjustmentsUpdate', function () {
			if (angular.equals({}, $scope.lampsLayer))
				return;
			// 
			// $emit event settings changed -> mod main obj -> emit event -> send to server -> // receve from server emit event
			//
			console.log('on adjustmentsUpdate - adjsServis');
			console.log(adjsServis);
			console.log('on adjustmentsUpdate - $scope.selectedFeatures');
			console.log($scope.selectedFeatures);

			driver_value = Math.round(255 * parseFloat(adjsServis.driver_value));
			dataSet = [];
			var prioritySet = function () {
				switch (adjsServis.flag) {
					case 'working_flag':
						return {
							"working_l_setting": driver_value,
							"working_flag": true
						};
					case 'presence_flag':
						return {
							"presence_l_setting": driver_value,
							"presence_flag": true
						};
					case 'special_flag':
						return {
							"special_l_setting": driver_value,
							"special_flag": true
						};
				}
			};

			$scope.selectedFeatures.forEach(function (feat) {
//				fgetProperties = feat.getProperties();
				var itemData = {
					id: feat.getId(),
//				group: [],
					change_required: true
				};
				angular.extend(itemData, prioritySet());
				console.log("itemData");
				console.log(itemData);
				dataSet.push(itemData);
			});
			console.log('dataSet');
			console.log(dataSet);

			// send data to server
			$scope.patchData(dataSet);
//			$scope.$emit('redrawLamps');
		});

		olData.getMap().then(function (map) {
			$scope.selectedFeatures = {};
			// add normal select interaction to handle click
			console.log('// add normal select interaction to handle click');
			select = new ol.interaction.Select({
				style: $scope.selectStyle
			});
			map.addInteraction(select);
			selectedFeatures = select.getFeatures();
			selectedFeatures.on(['add', 'remove'], function (e) {
//				$scope.$broadcast('selectFeatures', e.type);
				console.log("Features selected $scope.adjsServis.enable();")
				adjsServis.enable();
			});

			// a DragBox interaction used to select features by drawing boxes
			var dragBox = new ol.interaction.DragBox({
				condition: ol.events.condition.altKeyOnly,
				style: new ol.style.Style({
					stroke: new ol.style.Stroke({
						color: [0, 0, 255, 1]
					})
				})
			});
			map.addInteraction(dragBox);
			var infoBox = {}

			dragBox.on('boxend', function (e) {
				// features that intersect the box are added to the collection of
				// selected features, and their names are displayed in the "info"
				// div
				var info = [];
				var extent = dragBox.getGeometry().getExtent();
				var vectorSource = {};
				angular.forEach(map.getLayers(), function (layer) {
					if (layer.get('name') === 'lampsLayer') {
						vectorSource = layer.getSource();
					}
				});
				console.log('console.log(vectorSource);');
				console.log(vectorSource);
				vectorSource.forEachFeatureIntersectingExtent(extent, function (feature) {
					selectedFeatures.push(feature);
				});
			});
			// clear selection when drawing a new box and when clicking on the map
			dragBox.on('boxstart', function (e) {
				selectedFeatures.clear();
			});
			map.on('click', function () {
//							selectedFeatures.clear();
			});


			$scope.selectedFeatures = selectedFeatures;
		});
//		$scope.$watch('selectedFeatures', function (selectedFeatures) {
//			console.log("selectedFeatures");
//			console.log(selectedFeatures);
//		});


//		olData.getMap().then(function (map) {
//			var previousFeature,
//							hideTimeout;
//			var overlay = new ol.Overlay({
//				element: document.getElementById('overlaybox'),
//				positioning: 'center-center',
//				offset: [0, 0],
//				position: [0, 0]
//			});
//
//
//
//			var overlayHidden = true;
//			$scope.popupFeatureProperties = {};
//
//			// Mouse over function, called from the Leaflet Map Events
//			$scope.$on('openlayers.layers.lampsLayer.mousemove', function (event, feature, olEvent) {
////						$scope.$on('openlayers.map.pointermove', function (event, feature, olEvent) {
////							console.log(feature);
//				$timeout.cancel(hideTimeout);
//
//				$scope.$apply(function (scope) {
//					scope.popupFeatureProperties = feature.getProperties();
//				});
//				if (!feature) {
//					map.removeOverlay(overlay);
//					overlayHidden = true;
//					return;
//				} else if (overlayHidden) {
//					map.addOverlay(overlay);
//					overlayHidden = false;
//				}
//				hideTimeout = $timeout(function () {
////								return overlay.hide()
//					map.removeOverlay(overlay);
//					overlayHidden = true;
//				}, 7500);
//
//				overlay.setPosition(map.getEventCoordinate(olEvent));
//
////                if (feature) {
////                    feature.setStyle(olHelpers.createStyle({
////                        fill: {
////                            color: '#FFF'
////                        }
////                    }));
////
////                    if (previousFeature && feature !== previousFeature) {
////                        previousFeature.setStyle(previousFeature.getStyleFunction());
////                    }
////
////                    previousFeature = feature;
////                }
//			});
//		});








		$http.get('./json/layers.json').success(function (data) {
			console.log('Set layers maps');
			$scope.layers = data.response;
		});

		$http.get('./json/locations.json').success(function (data) {
			console.log('Set locations');
			$scope.locations = data.response;
		});


		$scope.$watch("offset", function (offset) {
			$scope.center.bounds[0] += parseFloat(offset, 10);
			$scope.center.bounds[1] += parseFloat(offset, 10);
			$scope.center.bounds[2] -= parseFloat(offset, 10);
			$scope.center.bounds[3] -= parseFloat(offset, 10);
			console.log("offset");
			console.log($scope.offset);
		});

		$scope.offsetFactor = 0.05;
		$scope.extentPlus = [];
		$scope.center.windowBounds = false;
//		$scope.$on('centerUrlHash', function () {


//ol.View.prototype.calculateExtent = function(size) {
//  var center = this.getCenter();
//  goog.asserts.assert(goog.isDef(center));
//  var resolution = this.getResolution();
//  goog.asserts.assert(goog.isDef(resolution));
//  var rotation = this.getRotation();
//  goog.asserts.assert(goog.isDef(rotation));
//  return ol.extent.getForViewAndSize(center, resolution, rotation, size);
//};


		$scope.$watch('center.bounds', function () {
			if ($scope.appHelpers.isValidBounds($scope.center.bounds)) {
				// add some margin... get scale or 1/zoom
				olData.getMap().then(function (map) {
					var wsize = [];
					var msize = map.getSize();
					wsize[0] = parseInt(msize[0] * (1 + parseInt($scope.offsetFactor)));
					wsize[1] = parseInt(msize[1] * (1 + parseInt($scope.offsetFactor)));
//					console.log(1 + parseInt($scope.offsetFactor));
//					console.log(msize);
//					console.log(wsize);
					var extentPlus = map.getView().calculateExtent(wsize);
					// or ol.extent.buffer()???
					$scope.extentPlus = ol.extent.applyTransform(extentPlus, ol.proj.getTransform("EPSG:3857", "EPSG:4326"));
					$scope.center.windowBounds = [
						//0 lb
						[$scope.extentPlus[0], $scope.extentPlus[1]],
						//1 lt
						[$scope.extentPlus[0], $scope.extentPlus[3]],
						//2 rt
						[$scope.extentPlus[2], $scope.extentPlus[3]],
						//3 rb
						[$scope.extentPlus[2], $scope.extentPlus[1]]
					];
				});
//				console.log("$scope.extentPlus");
//				console.log($scope.extentPlus);
//				console.log("$scope.center.bounds");
//				console.log($scope.center.bounds);
//				console.log("$scope.center.windowBounds");
//				console.log($scope.center.windowBounds);
			}
			;
		});


		// move to service
		// watch to on (emit getLampsEvent)
		$scope.$watch('center.windowBounds', function () {
			if ($scope.appHelpers.isValidBounds($scope.center.windowBounds)) {
//				console.log("windowBounds on windowBounds");
//				console.log($scope.center.windowBounds);
				$http({
//					method: 'GET',
					method: 'POST',
					url: 'http://10.1.2.55:8888/geolamps',
					data: $scope.center.windowBounds
				}).success(function (data) {
//					console.log("data on windowBounds");
//					console.log(data);
//					console.log('$scope.appHelpers.isResponse(data)');
//					console.log($scope.appHelpers.isResponse(data));
					if ($scope.appHelpers.isResponse(data)) {
						$scope.setLampsLayer(data);
						// redraw layer
						$scope.$emit('redrawLamps');
						console.log("$emit('redrawLamps')");
					}
				});
			}
		});

		$scope.patchData = function (pdata) {
			if (!$scope.appHelpers.isProperData(pdata))
				return;
			$http.patch('http://10.1.2.55:8888/lamps', pdata).
							success(function (data, status, headers, config) {
								// this callback will be called asynchronously
								// when the response is available
								console.log(data);
							}).
							error(function (data, status, headers, config) {
								// called asynchronously if an error occurs
								// or server returns response with an error status.
								console.log(data);
							});
		};

		$scope.$on('redrawLamps', function () {
			console.log('Redraw $scope.lampsLayer');
			// Refresh layer
			olData.getMap().then(function (map) {
				var layers = map.getLayers();
				// .map(layer.get('name') === 'lampsLayer')
				layers.forEach(function (layer) {
					if (layer.get('name') === 'lampsLayer') {
						var lSource = layer.getSource();
						var nf = lSource.readFeatures($scope.lampsSrc);//$scope.lData);
						lSource.clear(); //remove existing features
						lSource.addFeatures(nf);
						layer.setStyle($scope.lampsLayer.style);
					}
				});
			});
			$scope.setMarkers();
		});


//						TO DO????
//						lampsLayer.style.stroke <- breath
	}]);
