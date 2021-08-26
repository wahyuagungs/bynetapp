/**
 * Created by wahyuagungs on 23/2/19.
 */
angular.module('app').controller('ModelController', function ($scope, $http, $ngBootbox, $profileService) {

    function loadProjects() {
        $http.get('/api/project/list')
            .then(function (response) {
                if (response.data.status == 1) {
                    controller.projects = response.data.data;
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                    controller.projects = [];
                }

            }, function (response) {
                if (response.status == "403") {
                    $window.location.href = '/login';
                }
            }).catch(function (err) {
        });
    }

    var controller = this;
    controller.project = {};
    controller.scope = $scope;
    controller.scope.no = 1;
    controller.projects = [];
    controller.models = [];
    controller.show = false;
    controller.textArea = undefined;
    loadProjects();


    controller.progress = 10;

    controller.process = function (project) {
        controller.show = true;
        controller.project = project;
        loadModel(project);
    };

    function loadModel(project) {
        $http.get('/api/model/list', {
            params: {
                id: project.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {
                controller.models = data.data;
            } else {
                $ngBootbox.alert(data.message);
                controller.models = [];
            }
        });
    }

    controller.close = function () {
        controller.show = false;
        controller.project = {};
        controller.models = [];
    };

    $scope.uploadFile = function (files) {
        $scope.file = new FormData();
        $scope.file.append("file", files[0]);
        $scope.file.append("project_id", controller.project.id)
    };

    $scope.submitGuideDetailsForm = function () {
        $http.post('/uploadFile', $scope.file, {
            headers: {'Content-Type': undefined},
            transformRequest: angular.identity
        }).then(function (response) {
            console.log(response);
            data = response.data;
            if (data.status == 1) {
                $ngBootbox.alert(data);
                controller.project = {};
                controller.projects = [];
                controller.models = [];
                controller.show = false;
            } else {
                $ngBootbox.alert(data);
            }
        }, function (error) {
            $ngBootbox.alert(error.status + " " + error.statusText);
            // console.log(error);
        }).catch(function (err) {
        });
        $scope.file = {};
        loadModel(controller.project);
    };

    controller.saveTextModel = function () {
        var obj = {
            project_id : controller.project.id,
            data_content: controller.textArea
        };
        JSON.stringify(obj);
        $http.post('/api/model/save', obj)
            .then(function (response) {
                    data = response.data;
                    if (data.status == 1) {
                        controller.textArea = undefined;
                        $ngBootbox.alert(data.data);
                        loadModel(controller.project);
                    } else {
                        $ngBootbox.alert(data.message)
                            .then(function () {
                                return;
                            });
                    }
                }
            );
    };

    controller.constructModel = function (model) {
        $http.get('/api/model/load', {
            params: {
                id: model.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {
                loadModel(controller.project);

            } else {
                $ngBootbox.alert(data.message);
                // controller.models = [];
            }
        });
    };

    controller.activate = function (model) {
        $http.get('/api/model/activate', {
            params: {
                id: model.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {
                controller.models = data.data;
            } else {
                $ngBootbox.alert(data.message);
                controller.models = [];
            }
        });
    };

    controller.disable = function (model) {
        $http.get('/api/model/disable', {
            params: {
                id: model.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {
                controller.models = data.data;
            } else {
                $ngBootbox.alert(data.message);
                controller.models = [];
            }
        });
    };

});
