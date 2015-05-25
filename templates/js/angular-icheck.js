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

angular.module('angular-icheck', [])
				.directive('icheck', function ($timeout, $parse) {
					return {
						require: 'ngModel',
						link: function ($scope, element, $attrs, ngModel) {
							return $timeout(function () {
								var value = $attrs['value'];
								$scope.$watch($attrs['ngModel'], function (newValue) {
									$(element).iCheck('update');
								})

								$scope.$watch($attrs['ngDisabled'], function (newValue) {
									$(element).iCheck(newValue ? 'disable' : 'enable');
									$(element).iCheck('update');
								})

								return $(element).iCheck({
									checkboxClass: 'icheckbox_flat-aero',
									radioClass: 'iradio_flat-aero'
								}).on('ifToggled', function (event) {
									if ($(element).attr('type') === 'checkbox' && $attrs['ngModel']) {
										$scope.$apply(function () {
											return ngModel.$setViewValue(event.target.checked);
										});
									}
									if ($(element).attr('type') === 'radio' && $attrs['ngModel']) {
										return $scope.$apply(function () {
											return ngModel.$setViewValue(value);
										});
									}
								});
							}, 300);
						}
					};
				});