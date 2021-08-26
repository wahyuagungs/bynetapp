/**
 * Created by wahyuagungs on 22/2/19.
 */
angular.module('app').controller('ProfileController', function ($scope, $http, $ngBootbox, $profileService) {

    $scope.profile = $profileService.profile;
    $scope.user = $profileService.profile;
    $scope.passwords = {};

    $scope.updateProfile = function(){
        JSON.stringify($scope.user);
        $http.post('/api/user/profile/edit', $scope.user)
            .then(function(response){
               data = response.data;
               if(data.status == 1){
                   $ngBootbox.alert(data.data);
               } else{
                   $ngBootbox.alert(data.message);
               }
            });
    };

    $scope.updatePassword = function(){
        if ($scope.passwords.new1 != $scope.passwords.new2){
            $ngBootbox.alert('Your passwords do not match !');
            return;
        }
        var passwords = {old: $scope.passwords.old, new: $scope.passwords.new1};
        try{
            JSON.stringify(passwords);
        }catch (e){
            $ngBootbox.alert('Check your input ! ' + e);
            return;
        }
        $http.post('/api/user/profile/password', passwords)
            .then(function(response){
               data = response.data;
               if(data.status == 1){
                   $ngBootbox.alert(data.data);
                   $scope.resetPassword();
               } else{
                   $ngBootbox.alert(data.message);
               }
            });
    };

    $scope.resetUpdateProfile = function () {
        $scope.user = $profileService.profile;
    };

    $scope.resetPassword = function () {
        $scope.passwords = {};
    };

});