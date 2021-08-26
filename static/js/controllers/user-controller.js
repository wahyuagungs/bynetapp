angular.module('app').controller('UserManagementController', function ($scope, $http, $ngBootbox, $uibModal, ngTableParams, $window) {

    function initList(){
           controller.userPromise = $http.get('/api/user/list')
            .then(function(response){
                if (response.data.status == 1) {
                    $scope.tableParams = new ngTableParams({}, {dataset: response.data.data});
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $scope.tableParams = new ngTableParams({}, {dataset: []});
                    controller.data = [];
                    return;
                }

            },function(response){
                if (response.status == "403"){
                    $window.location.href = '/login';
                }
            }).catch(function (err) {});
    }

    var controller = this;
    controller.data = [];
    controller.scope = $scope;
    controller.scope.no = 1;
    controller.roles = [{'ref_role':1, 'name':'Administrator'},{'ref_role':3, 'name':'Participant'}];
    initList();

    controller.refresh = function(){
        initList();
    };


    controller.addUser = function(){
        controller.modalTitle = 'Add New User';
            var modalInstance = $uibModal
                .open({
                    scope: $scope,
                    templateUrl: "/static/views/modal/add_user.html?f",
                    controllerAs: 'addUserController',
                    controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                        var addUserController = this;
                        addUserController.modalTitle = controller.modalTitle;

                        addUserController.user = {};
                        addUserController.roles = controller.roles;
                        addUserController.submit = function(){
                            try{
                                var mandatoryObj = {
                                    "firstname": addUserController.user.firstname,
                                    "lastname" : addUserController.user.lastname,
                                    "username" : addUserController.user.username,
                                    "password" : addUserController.user.password
                                };
                                JSON.stringify(mandatoryObj);
                            }catch (e){
                                $ngBootbox.alert('Check your input ! ' + e);
                                return;
                            }

                            JSON.stringify(addUserController.user);
                            addUserController.postRequest = $http.post('/api/user/add', addUserController.user)
                                .then(function (response) {
                                    data = response.data;
                                    if(data.status == 1){
                                        $uibModalInstance.dismiss();
                                        initList();
                                    }else{
                                        $ngBootbox.alert(data.message)
                                            .then(function(){
                                                return;
                                            });
                                    }}
                                );
                        };

                        addUserController.cancel = function(){
                            $uibModalInstance.dismiss();
                        };

                    }]
                }).result.then(function(){console.log('ok')}, function(res){console.log('close');});
    };

    controller.editUser = function(obj){
        controller.modalTitle = 'Edit User';
            var modalInstance = $uibModal
                .open({
                    scope: $scope,
                    templateUrl: "/static/views/modal/edit_user.html?g",
                    controllerAs: 'editUserController',
                    controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                        var editUserController = this;

                        editUserController.modalTitle = controller.modalTitle;
                        editUserController.user = obj;
                        editUserController.user.password = null;

                        if (editUserController.user.roles[0]['ref_role'] == 1){
                            editUserController.user.role = controller.roles[0];
                        }else{
                            editUserController.user.role = controller.roles[1];
                        }

                        editUserController.roles = controller.roles;

                        editUserController.submit = function(){
                            try{
                                JSON.stringify(editUserController.user);
                            }catch (e){
                                $ngBootbox.alert('Check your input ! ' + e);
                                return;
                            }

                            JSON.stringify(editUserController.user);
                            editUserController.postRequest = $http.post('/api/user/edit', editUserController.user)
                                .then(function (response) {
                                    data = response.data;
                                        if(data.status == 1){
                                            $uibModalInstance.dismiss();
                                            initList();
                                        }else{
                                            $ngBootbox.alert(data.message)
                                                .then(function(){
                                                    return;
                                                });
                                        }
                                    }
                                )
                        };

                        editUserController.cancel = function(){
                            $uibModalInstance.dismiss();
                        };

                    }]
                }).result.then(function(){}, function(res){});
    };

    controller.delete = function (idx) {
        $ngBootbox.confirm('Do you want to delete this user?')
            .then(function(){
                $http.get('/api/user/delete', {
                    params: {
                        id: idx
                    }
                }).then(function (response) {
                    data = response.data;
                    if (data.status == 1){
                        initList();
                    } else {
                        $ngBootbox.alert(data.message);
                    }
                })
            }).catch(function (err) {});
    };

    controller.sendMail = function(idx){
        $ngBootbox.confirm('Do you want to send activation link?')
            .then(function(){
                $http.get('/api/user/sendmail', {
                    params: {
                        id: idx
                    }
                }).then(function (response) {
                    data = response.data;
                    if (data.status == 1){
                        initList();
                    } else {
                        $ngBootbox.alert(data.message);
                    }
                })
            }).catch(function (err) {});
    };
});