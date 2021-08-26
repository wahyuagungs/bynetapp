// Default colors
var brandPrimary =  '#20a8d8';
var brandSuccess =  '#4dbd74';
var brandInfo =     '#63c2de';
var brandWarning =  '#f8cb00';
var brandDanger =   '#f86c6b';

var grayDark =      '#2a2c36';
var gray =          '#55595c';
var grayLight =     '#818a91';
var grayLighter =   '#d1d4d7';
var grayLightest =  '#f8f9fa';


var Application = angular
.module('app', [
  'ui.router',
  'oc.lazyLoad',
  'ncy-angular-breadcrumb',
  'angular-loading-bar',
    "ui.bootstrap", 'ui.utils',
    'ngAnimate', 'ngSanitize',
    'ngTable', 'ngBootbox', 'cgBusy'
]);

Application.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
  cfpLoadingBarProvider.includeSpinner = false;
  cfpLoadingBarProvider.latencyThreshold = 1;
}]);

Application.run(['$rootScope', '$state', '$stateParams', function($rootScope, $state, $stateParams) {
  $rootScope.$on('$stateChangeSuccess',function(){
    document.body.scrollTop = document.documentElement.scrollTop = 0;
  });
  $rootScope.$state = $state;
  return $rootScope.$stateParams = $stateParams;
}]);

Application.service("$profileService", function () {
    this.profile = {};
    this.setProfile = function (profile) {
        this.profile = profile;
    };
});

Application.config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$breadcrumbProvider', function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider) {

  $urlRouterProvider.otherwise('/dashboard');

  $ocLazyLoadProvider.config({
    // Set to true if you want to see what and when is dynamically loaded
    debug: false
  });

  $breadcrumbProvider.setOptions({
    prefixStateName: 'app.main',
    includeAbstract: true,
    template: '<li class="breadcrumb-item" ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract"><a ng-switch-when="false" href="{{step.ncyBreadcrumbLink}}">{{step.ncyBreadcrumbLabel}}</a><span ng-switch-when="true">{{step.ncyBreadcrumbLabel}}</span></li>'
  });

  $stateProvider
  .state('app', {
    abstract: true,
    templateUrl: '/static/views/common/layouts/full.html',
    //page title goes here
    ncyBreadcrumb: {
      label: 'Root',
      skip: true
    },
    resolve: {
      loadCSS: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load CSS files
        return $ocLazyLoad.load([{
          serie: true,
          name: 'Font Awesome',
          files: ['/static/vendors/css/font-awesome.min.css']
        },{
          serie: true,
          name: 'Simple Line Icons',
          files: ['/static/vendors/css/simple-line-icons.css']
        }]);
      }],
      loadPlugin: ['$ocLazyLoad', function ($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load([{
          serie: true,
          name: 'chart.js',
          files: [
            '/static/vendors/js/Chart.min.js',
            '/static/vendors/js/angular-chart.min.js'
          ]
        }]);
      }],
    }
  })
  .state('app.main', {
    url: '/dashboard',
    templateUrl: '/static/views/dashboard.html?20190430_2020',
    controller: 'DashboardController',
    controllerAs: 'dashboardController',
    //page title goes here
    ncyBreadcrumb: {
      label: 'Home',
    },
    //page subtitle goes here
    params: { subtitle: 'Welcome to ByNet Application' },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load controllers
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/dashboard-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('appSimple', {
    abstract: true,
    templateUrl: '/static/views/common/layouts/simple.html',
    resolve: {
      loadCSS: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load CSS files
        return $ocLazyLoad.load([{
          serie: true,
          name: 'Font Awesome',
          files: ['/static/vendors/css/font-awesome.min.css']
        },{
          serie: true,
          name: 'Simple Line Icons',
          files: ['/static/vendors/css/simple-line-icons.css']
        }]);
      }],
    }
  })

}]);


/* Configuration for HTTP Interceptor for Session Timeout*/
Application.factory("httpInterceptor", ["$q", "$window",
    function ($q, $window) {
        return {
            response: function (response) {
                var responseHeaders;
                responseHeaders = response.headers();
                if (responseHeaders["content-type"] != undefined) {
                    if (responseHeaders["content-type"]
                            .indexOf("text/html") !== -1
                        && response.data
                        && response.data
                            .indexOf('<meta name="login" content="true">')
                        !== -1) {
                        $window.location.reload();
                        return $q.reject(response);
                    } else if (responseHeaders["content-type"]
                            .indexOf("text/html") !== -1
                        && response.data
                        && response.data
                            .indexOf('<meta name="500" content="true">')
                        !== -1) {
                        $window.location.reload();
                        return $q.reject(response);
                    }
                }
                return response;
            }
        };
    }
]);


Application.config([
    "$httpProvider",
    function ($httpProvider) {
        $httpProvider
            .interceptors.push("httpInterceptor");
    }
]);

Application.directive('d3Dagre', function () {
    return {
        restrict: 'A',
        link: function (scope, element) {
            var renderer = new dagreD3.render();

            var svg = d3.select("svg");
            var svgGroup = svg.append("g");

            renderer(d3.select("svg g"), scope.g);

            var xCenterOffset = (svg.attr("width") - scope.g.graph().width) / 2;
            svgGroup.attr("transform", "translate(" + xCenterOffset + ", 20)");
            svg.attr("height", scope.g.graph().height + 40);
            
            // var svg = d3.select("svg"),
            // width = svg.property("viewBox").baseVal.width,
            // height = svg.property("viewBox").baseVal.height,
            // radius = Math.min(width, height) / 2,
            // g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
        }
    }
});
