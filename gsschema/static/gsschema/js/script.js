var app = angular.module('gsschema',['ngCookies']);


app.controller('gsschema_ctrl', function($scope, $http, $q, $cookies, fileUpload){
    $scope.name = 'salam';
    $scope.layerList = [];
    $scope.isLoading = false;
    $scope.layerSelector = '';

    $scope.reloadLayers = function() {
        //TODO: show spinner
        $scope.isLoading = true;

        // server hasn't been added yet, so specify the auth headers here
        $http.get('/geoserver/wms?SERVICE=WMS&REQUEST=GetCapabilities').then(function(xhr) {
            $scope.layerList = [];
            if (xhr.status === 200) {
                var response = xhr.data;
                console.log(xhr.data);
                $(xhr.data).find('Layer').each(function(){
                    console.log('xo', $(this).children("Name").text());
                    var layerName = $(this).children("Name").text();
                    if (layerName) {
                        $scope.layerList.push($(this).children("Name").text());
                    }
			    });
            } else {
                // TODO: indicate that retrieving the layers has failed.
            }
            $scope.isLoading = false;
         }, function() {
            $scope.isLoading = false;
      });
    };

    // load years first time around
    $scope.reloadLayers();

    $scope.download = function() {
        var downloadUrl = '/gsschema/' + $scope.layerSelector + '/download';
        window.location = downloadUrl;
    };

    $scope.describe = function() {
        var downloadUrl = '/gsschema/' + $scope.layerSelector + '/describe';
        window.location = downloadUrl;
    };

    $scope.upload = function() {
        var file = $scope.myFile;
        console.log('file is ' );
        console.dir(file);
        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, '/gsschema/' + $scope.layerSelector + '/upload', $cookies.get('csrftoken'));
    };

});


app.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);


app.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl, csrfToken){
        var formData = new FormData();
        formData.append('file', file);
        $http.post(uploadUrl, formData, {
            transformRequest: angular.identity,
            headers: {
                'Content-Type': undefined,
                'X-CSRFToken': csrfToken
            }
        }
        ).success(function(){
        }).error(function(){
        });
    }
}]);