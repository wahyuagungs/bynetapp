/**
 * Created by wahyuagungs on 24/2/19.
 */
angular.module('app').controller('ProfileAppController', function ($scope, $http, $ngBootbox, $profileService) {

    function load(){
        $http.get('/api/profile/app')
            .then(function(response){
                if (response.data.status == 1) {
                    if (response.data.data != 0)
                        controller.profileApp = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    controller.profileApp = {};
                }
            },function(response){
            }).catch(function (err) {});
    }

    var controller = this;
    controller.profileApp = {};
    controller.scope = $scope;
    load();

    controller.save = function () {
        if (JSON.stringify(controller.profileApp) == JSON.stringify({})){
            $ngBootbox.alert('Please fill out the form !');
            return;
        }
        JSON.stringify(controller.profileApp);
        $http.post('/api/profile/save', controller.profileApp)
            .then(function (response) {
                    data = response.data;
                    if (data.status == 1) {
                        $ngBootbox.alert(data.data);
                    } else {
                        $ngBootbox.alert(data.message)
                            .then(function () {
                                return;
                            });
                    }
                }
            );
    };

    controller.reset = function () {
        controller.profileApp = {};
    };


});
