angular.module('app').controller('ViewTaskController', function ($scope, $http, $ngBootbox) {

    function loadProjects() {
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
    $ctrl.show = false;
    $ctrl.scope.no = 1;
    $ctrl.projects = [];
    $ctrl.scope.g = {};
    loadProjects();

    var nodes = [];
    var arcs = [];

    $ctrl.view = function (project) {
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
                    if (arc.parent_id != null){
                        g.setEdge(arc.parent_id, arc.child_id);
                    }
                });

                $ctrl.scope.g = g;
                console.log(g);
                $ctrl.show = true;
            } else {
                nodes = [];
                arcs = [];
                $ngBootbox.alert(data.message);
            }
        });
    };

    $ctrl.close = function () {
        $ctrl.show = false;
    };

});
