// controller.js
Application.controller('sidebarController', function($scope, $http){
    $scope.menuItem = {};
    $scope.menutItems = [];

    $scope.menuList = $http.get('api/menu')
        .then(function (response) {
            data = response.data;
            if (data.status == 1) {
                $scope.menuItems = data.data;
            }
        });
});


Application.controller('headerController', function($scope, $http, $profileService, $location){
    var profile={};
    $scope.userProfile = $http.get('api/user/profile')
        .then(function(response){
            data = response.data;
            profile = data.data;
            $profileService.setProfile(profile);
            $scope.profile = profile;
            if (profile.roles[0].ref_role == 3){
                $location.path('/tasks/process');
            }
        });
});