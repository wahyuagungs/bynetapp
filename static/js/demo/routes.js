angular
.module('app')
.config(['$stateProvider', '$urlRouterProvider', '$ocLazyLoadProvider', '$breadcrumbProvider', function($stateProvider, $urlRouterProvider, $ocLazyLoadProvider, $breadcrumbProvider) {
  $stateProvider
  .state('app.icons', {
    url: "/icons",
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: 'Icons'
    }
  })
  .state('app.contact', {
    url: '/about',
    templateUrl: '/static/views/about.html?20190430_2020',
    controller: 'AboutController',
    controllerAs: 'aboutController',
    ncyBreadcrumb: {
      label: 'About'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/about-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('app.settings', {
    url: "/settings",
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: 'Settings'
    }
  })
  .state('app.settings.user', {
    url: '/user',
    templateUrl: '/static/views/user-management.html?20190430_2020',
    controller: 'UserManagementController',
    controllerAs: 'userController',
    ncyBreadcrumb: {
      label: 'Manage Users'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/user-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('app.settings.profile', {
    url: '/profile',
    templateUrl: '/static/views/app-profile.html?20190430_2020',
    controller: 'ProfileAppController',
    controllerAs: 'profileAppController',
    ncyBreadcrumb: {
      label: 'Application Profile Setting'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/profileapp-controller.js?20190430_2020']
        });
      }]
    }
  })
   .state('app.project', {
    url: "/project",
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: 'Projects'
    }
  })
  .state('app.project.manage', {
    url: '/create',
    templateUrl: '/static/views/manage-project.html?20190430_2020',
    controller: 'ProjectController',
    controllerAs: 'projectController',
    ncyBreadcrumb: {
      label: 'Manage Projects'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/project-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('app.project.info', {
    url: '/info',
    templateUrl: '/static/views/project-info.html?20190430_2020',
    controller: 'ProjectInfoController',
    controllerAs: 'projectInfoController',
    ncyBreadcrumb: {
      label: 'Project Information Schema'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/projectinfo-controller.js?20190430_2020']
        });
      }]
    }
  })
   .state('app.project.model', {
    url: '/model',
    templateUrl: '/static/views/manage-model.html?20190430_2020',
    controller: 'ModelController',
    controllerAs: 'modelController',
    ncyBreadcrumb: {
      label: 'Manage Models'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/model-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('app.tasks', {
    url: "/tasks",
    abstract: true,
    template: '<ui-view></ui-view>',
    ncyBreadcrumb: {
      label: 'Projects'
    }
  })
  .state('app.tasks.view', {
    url: '/view',
    templateUrl: '/static/views/view-task.html?20190430_2020',
    controller: 'ViewTaskController',
    controllerAs: 'viewTaskController',
    ncyBreadcrumb: {
      label: 'View Tasks'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: [
              '/static/js/controllers/viewtask-controller.js?20190430_2020'
          ]
        });
      }]
    }
  })
  .state('app.tasks.process', {
    url: '/process',
    templateUrl: '/static/views/process-task.html?20190430_2020',
    controller: 'ProcessTaskController',
    controllerAs: 'processTaskController',
    ncyBreadcrumb: {
      label: 'Process Tasks'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/processtask-controller.js?20190430_2020']
        });
      }]
    }
  })
  .state('app.profile', {
    url: '/profile',
    templateUrl: '/static/views/profile.html?20190430_2020',
    controller: 'ProfileController',
    controllerAs: 'profileController',
    ncyBreadcrumb: {
      label: 'Profile Account'
    },
    resolve: {
      loadMyCtrl: ['$ocLazyLoad', function($ocLazyLoad) {
        // you can lazy load files for an existing module
        return $ocLazyLoad.load({
          files: ['/static/js/controllers/profile-controller.js?20190430_2020']
        });
      }]
    }
  })
}]);
