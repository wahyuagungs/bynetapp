/**
 * Created by wahyuagungs on 23/2/19.
 */
angular.module('app').controller('ProjectController', function ($scope, $http, $ngBootbox, $profileService, $uibModal, ngTableParams, $window, $filter) {

    function initList() {
        $http.get('/api/project/list')
            .then(function (response) {
                if (response.data.status == 1) {
                    $scope.tableParams = new ngTableParams({}, {dataset: response.data.data});
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $scope.tableParams = new ngTableParams({}, {dataset: []});
                    controller.data = [];
                    return;
                }

            }, function (response) {
                if (response.status == "403") {
                    $window.location.href = '/login';
                }
            }).catch(function (err) {
        });
    }

    var controller = this;
    controller.data = [];
    controller.project_users = [];
    controller.scope = $scope;
    controller.scope.no = 1;
    controller.show = false;
    controller.project = {};
    initList();

    controller.refresh = function () {
        initList();
    };

    $scope.open1 = function () {
        $scope.popup1.opened = true;
    };

    $scope.popup1 = {
        opened: false
    };

    $scope.open2 = function () {
        $scope.popup2.opened = true;
    };

    $scope.popup2 = {
        opened: false
    };

    controller.add = function () {
        controller.modalTitle = 'Add New Project';
        var modalInstance = $uibModal
            .open({
                scope: $scope,
                templateUrl: "/static/views/modal/add_project.html?a",
                controllerAs: 'addProjectController',
                controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                    var addProjectController = this;
                    addProjectController.modalTitle = controller.modalTitle;

                    addProjectController.project = {};
                    addProjectController.submit = function () {
                        JSON.stringify(addProjectController.project);
                        addProjectController.postRequest = $http.post('/api/project/add', addProjectController.project)
                            .then(function (response) {
                                    data = response.data;
                                    if (data.status == 1) {
                                        $uibModalInstance.dismiss();
                                        initList();
                                    } else {
                                        $ngBootbox.alert(data.message)
                                            .then(function () {
                                                return;
                                            });
                                    }
                                }
                            ).catch(function (error) {
                                console.log(error);
                            });
                    };

                    addProjectController.cancel = function () {
                        $uibModalInstance.dismiss();
                    };


                }]

            }).result.then(function () {
                console.log('ok')
            }, function (res) {
                console.log('Error');
            });
    };

    controller.edit = function (obj) {
        controller.modalTitle = 'Edit Project';
        var modalInstance = $uibModal
            .open({
                scope: $scope,
                templateUrl: "/static/views/modal/edit_project.html?a",
                controllerAs: 'editProjectController',
                controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                    var editProjectController = this;
                    editProjectController.modalTitle = controller.modalTitle;

                    editProjectController.project = obj;
                    editProjectController.project.start_date = new Date(obj.start_date);
                    editProjectController.project.end_date = new Date(obj.end_date);

                    editProjectController.submit = function () {
                        JSON.stringify(editProjectController.project);
                        editProjectController.postRequest = $http.post('/api/project/edit', editProjectController.project)
                            .then(function (response) {
                                    data = response.data;
                                    if (data.status == 1) {
                                        $uibModalInstance.dismiss();
                                        initList();
                                    } else {
                                        $ngBootbox.alert(data.message)
                                            .then(function () {
                                                return;
                                            });
                                    }
                                }
                            ).catch(function (error) {
                                console.log(error);
                            });
                    };

                    editProjectController.cancel = function () {
                        $uibModalInstance.dismiss();
                    };
                }]
            }).result.then(function () {
            }, function (res) {
            });
    };

    controller.select = function (project) {
        controller.show = true;
        controller.project = project;
        userList(project);
    };

    function userList(project) {
        $http.get('/api/project/users', {
            params: {
                id: project.id
            }
        }).then(function (response) {
            if (response.data.status == 1) {
                // $scope.tableAssign = new ngTableParams({}, {});
                controller.project_users = response.data.data;
            } else if (response.data.status == 0) {
                $ngBootbox.alert(response.data.message);
                // $scope.tableAssign = new ngTableParams({}, {dataset: []});
                controller.project_users = [];
            }
        }, function (response) {
            if (response.status == "403") {
                $window.location.href = '/login';
            }
        }).catch(function (err) {
        });
    }

    controller.refreshAssignments = function(){
        userList(controller.project);
    };

    controller.assignUser = function () {
        controller.modalTitle = 'Assign User';
        var modalInstance = $uibModal
            .open({
                scope: $scope,
                templateUrl: "/static/views/modal/assign_user.html?a",
                controllerAs: 'assignController',
                size: 'lg',
                controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                    var assignController = this;
                    assignController.modalTitle = controller.modalTitle;

                    $http.get('/api/user/list/active')
                        .then(function(response){
                            if (response.data.status == 1) {
                                $scope.tableUsers = new ngTableParams({}, {dataset: response.data.data});
                            } else if (response.data.status == 0) {
                                $ngBootbox.alert(response.data.message);
                                $scope.tableUsers = new ngTableParams({}, {dataset: []});
                                controller.data = [];
                                return;
                            }
                        },function(response){
                            if (response.status == "403"){
                                $window.location.href = '/login';
                            }
                        }).catch(function (err) {});

                    assignController.choose = function(user){
                        if (controller.project_users.length < controller.project.max_participants){
                            var found = $filter('filter')(controller.project_users, {'id': user.id}, true);
                            if (found.length) {
                                $ngBootbox.alert('User already existed !');
                                $uibModalInstance.dismiss();
                                return;
                            }
                            user.temp = true;
                            controller.project_users.push(user);
                        }else{
                            $ngBootbox.alert('Maximum Participants reached !');
                        }
                        $uibModalInstance.dismiss();
                    };
                    assignController.cancel = function () {
                        $uibModalInstance.dismiss();
                    };
                }]
            }).result.then(function () {
            }, function (res) {
            });
    };

    controller.close = function () {
        controller.show = false;
        controller.project = {};
    };

    controller.delete = function (idx) {
        $ngBootbox.confirm('Do you want to deactivate the project?')
            .then(function () {
                $http.get('api/project/delete', {
                    params: {
                        id: idx
                    }
                }).then(function (response) {
                    data = response.data;
                    if (data.status == 1) {
                        initList();
                    } else {
                        $ngBootbox.alert(data.message);
                    }
                })
            }, function () {

            });
    };

    controller.deleteUser = function(user){
        $ngBootbox.confirm('Do you want to remove this person from current project?')
            .then(function () {
                $http.get('api/project/users/delete', {
                    params: {
                        project_id: controller.project.id,
                        user_id: user.id
                    }
                }).then(function (response) {
                    data = response.data;
                    if (data.status == 1) {
                        userList(controller.project);
                    } else {
                        $ngBootbox.alert(data.message);
                    }
                })
            }, function () {

            });
    };

    controller.saveProjectUsers = function () {
        if (controller.project_users.length == 0){
            $ngBootbox.alert('No Data to save !');
            return;
        }
        var obj = {
            'project_id' : controller.project.id,
            'data': controller.project_users
        };
        JSON.stringify(obj);
        $http.post('/api/project/users/save', obj)
            .then(function (response) {
                data = response.data;
                if(data.status == 1){
                    userList(controller.project);
                }else{
                    $ngBootbox.alert(data.message)
                        .then(function(){
                            return;
                        });
                }}
            );
    };

});
