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

// chenge to directive
app.controller('lmsLuxMeter', ['$scope', function($scope) {
    var lux;
    var luxTooBig = 0;

    window.addEventListener('devicelight', function(e) {
        var luxRaw = e.value.toString();
        if (luxRaw.length < 4) {
            lux = '';
            for (i = 0; i < (4 - luxRaw.length); i++)
                lux += '0';
            lux += luxRaw;
            luxTooBig = 0;
        } else {
            if (luxRaw.length > 4) {
                lux = luxRaw.substring(0, 4);
                luxTooBig = 1;
            } else {
                lux = luxRaw;
                luxTooBig = 0;
            }
        }
        screenValue = lux.replace('1', ' 1');
        $scope.$apply(function() {
            $scope.currentLuxVal = lux;
        });
    });
}]);
