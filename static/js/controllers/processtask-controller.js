angular.module('app').controller('ProcessTaskController', function ($scope, $http, $ngBootbox, $uibModal) {

    function loadActiveModel() {
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
    $ctrl.projects = [];
    $ctrl.models = [];
    $ctrl.model = {};
    $ctrl.show = false;

    $ctrl.stage = 0;
    $ctrl.display = {};

    loadActiveModel();

    $scope.radioModel = null;
    $ctrl.checkModel = {};
    $ctrl.checkResults = [];

    $ctrl.startSurvey = function (project) {
        $http.get('/api/task/survey/start', {
            params: {
                id: project.model.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {
                surveyBegins(project);
            } else {
                $ngBootbox.alert(data.message);
            }
        }, function (response) {
        })
            .catch(function (err) {
            });
    };

    $ctrl.continueSurvey = function (project) {
        surveyBegins(project);
    };

    function surveyBegins(project) {
       $ctrl.taskPromise = $http.get('/api/task/survey/process', {
            params: {
                id: project.model.id
            }
        }).then(function (response) {
            data = response.data;
            if (data.status == 1) {

                $ctrl.stage = data.data.stage;

                $ctrl.display.statement = data.data.statement;
                $ctrl.display.variable = data.data.variable;
                $ctrl.display.ep_id = data.data.ep_id;
                $ctrl.display.condition = data.data.condition;
                $ctrl.show = true;
                $ctrl.project = project;
                $ctrl.display.progress =  data.data.progress;

                if (data.data.stage == 3) {
                    $ctrl.display.parents = data.data.parents;
                    $ctrl.display.objects = {};
                } else if (data.data.stage == 4) {
                    $ctrl.display.variables = data.data.variables;
                    $ctrl.display.cpc_id = data.data.cpc_id;
                } else if (data.data.stage == 5) {
                    $ctrl.display.conditions = data.data.conditions;
                } else if (data.data.stage == 6) {
                    $ctrl.display.tags = data.data.tags;
                    $ctrl.display.var_alloc_id = data.data.var_alloc_id;
                }
            } else {
                $ngBootbox.alert(data.message);
                $ctrl.display = {};
            }
        }, function (response) {
        })
            .catch(function (err) {
            });
    }

    $ctrl.next = function () {
        var save = {};
        save.stage = $ctrl.stage;
        if ($ctrl.stage < 3 || $ctrl.stage == 5) {
            if ($ctrl.radioModel == null) {
                $ngBootbox.alert("Please select one of the options provided ");
                return;
            } else {
                save = {
                    model_id: $ctrl.project.model.id,
                    ep_id: $ctrl.display.ep_id,
                    value: $ctrl.radioModel,
                    stage: $ctrl.stage
                };
            }
        } else if ($ctrl.stage == 3) {
            if (Object.keys($ctrl.display.objects).length != $ctrl.display.parents.length) {
                $ngBootbox.alert("Please fill up all options");
                return;
            } else {
                save = JSON.parse(JSON.stringify($ctrl.display.objects));
                save.stage = 3;
                save.model_id = $ctrl.project.model.id;
            }
        } else if ($ctrl.stage == 4) {
            if (Object.keys($ctrl.radioModel).length != $ctrl.display.variables.length) {
                $ngBootbox.alert("Please fill up all options");
                return;
            } else {
                save.cpc_state = JSON.parse(JSON.stringify($ctrl.radioModel));
                save.cpc_id = $ctrl.display.cpc_id;
                save.model_id = $ctrl.project.model.id;
            }
        } else if ($ctrl.stage == 6) {
            if ($ctrl.checkResults.length == 0){
                $ngBootbox.alert("Please select at least one of the categories");
                return;
            } else {
                save.tags = $ctrl.checkResults;
                save.model_id = $ctrl.project.model.id;
                save.var_alloc_id = $ctrl.display.var_alloc_id;
            }
        }

        JSON.stringify(save);
       $ctrl.taskPromise = $http.post('/api/task/survey/process', save)
            .then(function (response) {
                data = response.data;
                if (data.status == 1) {
                    $ctrl.stage = data.data.stage;

                    if ($ctrl.stage.stage == 9){
                        //finish
                    }

                    $ctrl.display.statement = data.data.statement;
                    $ctrl.display.variable = data.data.variable;
                    $ctrl.display.ep_id = data.data.ep_id;
                    $ctrl.display.condition = data.data.condition;
                    $ctrl.display.progress =  data.data.progress;

                    $ctrl.show = true;
                    $ctrl.radioModel = null;
                    $ctrl.checkModel = {};
                    $ctrl.checkResults = [];

                    if (data.data.stage == 3) {
                        $ctrl.display.parents = data.data.parents;
                        $ctrl.display.objects = {};
                    } else if (data.data.stage == 4) {
                        $ctrl.display.variables = data.data.variables;
                        $ctrl.display.cpc_id = data.data.cpc_id;
                    } else if (data.data.stage == 5) {
                        $ctrl.display.conditions = data.data.conditions;
                    } else if (data.data.stage == 6) {
                        $ctrl.display.tags = data.data.tags;
                        $ctrl.display.var_alloc_id = data.data.var_alloc_id;
                    }

                } else {
                    $ngBootbox.alert(data.message);
                    return;
                }
            });
    };


    $ctrl.nextTest = function () {
        console.log($ctrl.checkResults);
        if ($ctrl.checkResults.length == 0){
            $ngBootbox.alert('Empty');
        }
    };


    $ctrl.back = function () {
        $ctrl.project = {};
        $ctrl.display = {};
        $ctrl.stage = 0;
        $ctrl.model = {};
        $ctrl.checkResults = [];
        $ctrl.show = false;
        loadActiveModel();
    };

    $ctrl.percentage = function (textChosen) {
        var text = '';
        if (textChosen == 'Impossible') {
            text = '0% occurrences';
        } else if (textChosen == 'Improbable') {
            text = '15% occurrences';
        } else if (textChosen == 'Uncertain') {
            text = '25% occurrences';
        } else if (textChosen == 'Fifty-fifty') {
            text = '50% occurrences';
        } else if (textChosen == 'Expected') {
            text = '75% occurrences';
        } else if (textChosen == 'Probable') {
            text = '85% occurrences';
        } else if (textChosen == 'Certain') {
            text = '100% occurrences';
        }
        return text;
    };

    $ctrl.pushTag = function (tag_id) {
        var idx = $ctrl.checkResults.indexOf(tag_id);
        if (idx >= 0) {
            $ctrl.checkResults.splice(idx, 1);
        } else {
            $ctrl.checkResults.push(tag_id);
        }
    };

    $ctrl.addTag = function () {
        var modalTitle = 'Add New Category';
        var modalInstance = $uibModal
            .open({
                scope: $scope,
                templateUrl: "/static/views/modal/add_tag.html?20190430_2020",
                controllerAs: 'addTagController',
                controller: ['$scope', '$uibModalInstance', function ($scope, $uibModalInstance) {
                    var addTagController = this;
                    addTagController.modalTitle = modalTitle;

                    addTagController.tag = {};
                    addTagController.tag.model_id = $ctrl.project.model.id;
                    addTagController.submit = function () {
                        JSON.stringify(addTagController.tag);
                        addTagController.postRequest = $http.post('/api/model/tag/add', addTagController.tag)
                            .then(function (response) {
                                    data = response.data;
                                    if (data.status == 1) {
                                        $uibModalInstance.dismiss();
                                        loadTag();
                                    } else {
                                        $ngBootbox.alert(data.message)
                                            .then(function () {
                                                return;
                                            });
                                    }
                                }
                            );
                    };

                    addTagController.cancel = function () {
                        $uibModalInstance.dismiss();
                    };

                }]
            }).result.then(function () {
                console.log('ok')
            }, function (res) {
                console.log('close');
            });
    };

    function loadTag() {
        $ctrl.tagPromise = $http.get('/api/model/tag/list', {
                params: {
                    id: $ctrl.project.model.id
                }
            }).then(function (response) {
                if (response.data.status == 1) {
                    $ctrl.display.tags = response.data.data;
                    $ctrl.checkResults = [];
                } else if (response.data.status == 0) {
                    $ngBootbox.alert(response.data.message);
                }
            }, function (response) {
            }).catch(function (err) {
        });
    }

    $ctrl.skip = function() {

    };

});
