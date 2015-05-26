/* 
 * Copyright (C) Error: on line 4, column 33 in Templates/Licenses/license-gpl30.txt
 The string doesn't match the expected date/time format. The string to parse was: "13-May-2015". The expected format was: "MMM d, yyyy". miko
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
//			id
//			identifier
//			actual_driver_value
//			wanted_l_level
//			working_flag
//			working_l_setting
//			presence_flag
//			presence_l_setting
//			special_flag
//			special_l_setting
//			change_required
//			group
//			hardware.building
//			hardware.protocol
//			hardware.is_sensor
//			hardware.computer_ip
//			hardware.address
//			hardware.type
//			location.type
//			location.coordinates

app.factory('adjsServis', ['$rootScope', function ($rootScope) {
		var adjustments = {
			"isDisabled": true,
			"driver_value": 80,
			"flag": 'special_flag',
			"enable": function () {
				adjustments.isDisabled = false;
				$rootScope.$broadcast('adjustmentsEnabled');
				console.log("Adjs form enable");
			},
			"disable": function () {
				adjustments.isDisabled = true;
				$rootScope.$broadcast('adjustmentsDisabled');
				console.log("Adjs form disable");
			},
			"setAdjs": function () {
				$rootScope.$broadcast('adjustmentsUpdate');
				console.log("Adjs form update!");
			}
		};
		return adjustments;
	}]);

app.controller('lmsControlPanel', ['$scope', 'adjsServis', function ($scope, adjsServis) {
		var updateAdjs = function () {
			$scope.adjustment = adjsServis;
		};

		$scope.$on('adjustmentsEnabled', function () {
			//$scope.$watch('adjustment', function () {
			console.log("$scope.adjsServis just changed!!!");
			$scope.$apply(
							updateAdjs()
							);
			console.log($scope.adjustment);
		});

		updateAdjs();

//		$scope.$watch('adjustment', function () {
//			console.log($scope.adjustment);
//		}, true);
		$scope.setAdjs = adjsServis.setAdjs
	}]);