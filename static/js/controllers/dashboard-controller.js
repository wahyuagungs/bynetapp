angular.module('app').controller('DashboardController', function ($scope, $http, $ngBootbox, $profileService, $uibModal) {

    function getUserProfile() {
        $http.get('api/user/profile')
            .then(function (response) {
                data = response.data;
                profile = data.data;
                $profileService.setProfile(profile);
                $ctrl.profile = profile;
                $ctrl.profile.role = $ctrl.profile.roles[0].ref_role;
            });
    }

    function getDashboardInformation() {
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

    function getTaskList() {
        $http.get('/api/task/list')
            .then(function (response) {
                if (response.data.status == 1) {
                    $ctrl.projects = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    $ctrl.projects = [];
                }
            }, function (response) {
            }).catch(function (err) {
        });
    }

    var $ctrl = this;
    $ctrl.scope = $scope;
    $scope.no = 1;
    $ctrl.profile = {};
    $ctrl.profileApp = {};
    $ctrl.logs = [];
    $ctrl.recents = [];
    $ctrl.projects = [];

    $ctrl.profile = {};

    getUserProfile();

    getDashboardInformation();

    getTaskList();
    $scope.g = {};
    $scope.show = false;

    $scope.view = function (project) {
        var modalTitle = 'View Model';
        var nodes = [];
        var arcs = [];
        var modalInstance = $uibModal
            .open({
                scope: $scope,
                templateUrl: "/static/views/modal/view_model.html?F",
                controllerAs: 'modelController',
                size: 'lg',
                controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                    var modelController = this;
                    modelController.show = false;
                    modelController.modalTitle = modalTitle;
                    $http.get('/api/task/model/get', {
                        params: {
                            id: project.model.id
                        }
                    }).then(function (response) {
                        data = response.data;
                        if (data.status == 1) {
                            nodes = data.data.nodes;
                            arcs = data.data.arcs;
                            var g = new dagreD3.graphlib.Graph().setGraph({});
                            g.setGraph({});
                            g.setDefaultEdgeLabel(function () {
                                return {};
                            });
                            nodes.forEach(function (node) {
                                g.setNode(node.id, {label: node.label});
                            });

                            arcs.forEach(function (arc) {
                                if (arc.parent_id != null) {
                                    g.setEdge(arc.parent_id, arc.child_id);
                                }
                            });
                            $scope.g = g;
                            modelController.show = true;
                        } else {
                            nodes = [];
                            arcs = [];
                            $ngBootbox.alert(data.message);
                        }
                    });



                    modelController.cancel = function () {
                        $uibModalInstance.dismiss();
                    };

                }]
            }).result.then(function () {
            }, function (res) {
                $scope.g = {};
            });


    };

});
