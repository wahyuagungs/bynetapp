angular.module('app').controller('AboutController', function ($scope, $http, $ngBootbox) {

    function getDashboardInformation(){
        // get information
        $http.get('/api/dashboard/information')
            .then(function (response) {
                if (response.data.status == 1) {
                    $ctrl.profileApp = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $ctrl.profileApp = {};
                }
            }, function (response) {
            }).catch(function (err) {
        });
        // get access
        $http.get('/api/dashboard/access')
            .then(function (response) {
                if (response.data.status == 1) {
                    $ctrl.logs = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $ctrl.logs = [];
                }
            }, function (response) {
            }).catch(function (err) {
        });
        // get recents
        $http.get('/api/dashboard/recent')
            .then(function (response) {
                if (response.data.status == 1) {
                    $ctrl.recents = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $ctrl.recents = [];
                }
            }, function (response) {
            }).catch(function (err) {
        });
    }

    var $ctrl = this;
    $ctrl.scope = $scope;
    $ctrl.profileApp = {};
    $ctrl.logs = [];
    $ctrl.recents = [];

    getDashboardInformation();



});
