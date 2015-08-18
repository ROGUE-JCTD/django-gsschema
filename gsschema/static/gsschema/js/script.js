var app = angular.module('gsschema',['ngCookies']);

if(!String.prototype.startsWith){
    String.prototype.startsWith = function (str) {
        return !this.indexOf(str);
    }
}

app.controller('gsschema_ctrl', function($scope, $http, $q, $cookies, fileUpload, fileRemove){
    $scope.name = 'salam';
    $scope.layerList = [];
    $scope.isLoading = false;
    $scope.layerSelector = '';
    $scope.hasValidSchema = false;
    $scope.canRemoveFile = false;
    $scope.hasUploadFile = false;

    $scope.reloadLayers = function() {
        $scope.isLoading = true;

        // server hasn't been added yet, so specify the auth headers here
        $http.get('/geoserver/wms?SERVICE=WMS&REQUEST=GetCapabilities').then(function(xhr) {
            $scope.layerList = [];
            if (xhr.status === 200) {
                var response = xhr.data;
                $(xhr.data).find('Layer').each(function(){
                    console.log('xo', $(this).children("Name").text());
                    var layerName = $(this).children("Name").text();
                    if (layerName) {
                        $scope.layerList.push($(this).children("Name").text());
                    }
			    });
            } else {
                window.alert("There was a problem retrieving the layers from the server. Please make sure you're logged into GeoShape.")
            }
            $scope.isLoading = false;
         }, function() {
            $scope.isLoading = false;
      });
    };

    // load years first time around
    $scope.reloadLayers();

    $scope.showButtons = function() {
        if ($scope.layerSelector){
            return true;
        } else {
            return false;
        }
    };

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
        console.dir(file);

        var uploadUrl = '/gsschema/' + $scope.layerSelector + '/upload';
        fileUpload.uploadFileToUrl(file, uploadUrl, $cookies.get('csrftoken')).then(function(response) {
            $scope.hasValidSchema = true;
            $scope.canRemoveFile = true;
            // remove the file since it succeeded
            $('input[type="file"]').val('');
            console.log(response);
            window.alert('Upload Successful!');
        }, function(reject) {
            console.log(reject);
            window.alert(reject);
        });
    };

    $scope.remove = function() {
        var confirm = window.confirm("Are you sure you want to remove the file?");

        $scope.tt_isOpen = false; // Close tooltip
        if (confirm === true) {
            // OK
            var removeUrl = '/gsschema/' + $scope.layerSelector + '/remove/';
            fileRemove.removeFileWithUrl(removeUrl).then(function(response){
                $scope.hasValidSchema = false;
                $scope.canRemoveFile = false;
                console.log(response);
            }, function(reject) {
                console.log(reject);
                window.alert(reject);
            });
        } else {
            // Cancel
        }
    };

    $scope.hasValidFile = function() {
        if ($scope.layerSelector) {
            var downloadUrl = '/gsschema/' + $scope.layerSelector + '/download';
            $http.get(downloadUrl).then(function(xhr){
                if (xhr.status === 200){
                    if (!xhr.data.startsWith('Error')){
                        $scope.hasValidSchema = true;
                        $scope.canRemoveFile = true;
                    } else {
                        $scope.hasValidSchema = false;
                        $scope.canRemoveFile = false;
                    }
                } else {
                    $scope.hasValidSchema = false;
                    $scope.canRemoveFile = false;
                }
            });
        }
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
                    if (element[0].files.length > 0){
                        scope.hasUploadFile = true;
                    } else {
                        scope.hasUploadFile = false;
                    }
                });
            });
        }
    };
}]);

app.directive('toggle', function(){
  return {
    restrict: 'A',
    link: function(scope, element, attrs){
      if (attrs.toggle=="tooltip"){
        $(element).tooltip({container: 'body'});
      }
    }
  };
})

app.service('fileUpload', ['$http', '$q', function ($http, $q) {
    this.uploadFileToUrl = function(file, uploadUrl, csrfToken){
        var deferredResponse = $q.defer();
        var formData = new FormData();
        formData.append('file', file);
        $http.post(uploadUrl, formData, {
            transformRequest: angular.identity,
            headers: {
                'Content-Type': undefined,
                'X-CSRFToken': csrfToken
            }
        }
        ).success(function(response){
            if (!response.startsWith('Error')){
                deferredResponse.resolve(response);
            } else {
                deferredResponse.reject(response);
            }
        }).error(function(){
            deferredResponse.reject('There was problem uploading the file. Please check your network connectivity and try again.');
        });
        return deferredResponse.promise;
    }
}]);

app.service('fileRemove', ['$http', '$q', function($http, $q) {
    this.removeFileWithUrl = function(fileUrl){
        var deferredResponse = $q.defer();
        $http.get(fileUrl).then(function(response){
            // URL returned successfully
            if (!response.data.startsWith('Error')){
                deferredResponse.resolve(response.data);
            } else {
                deferredResponse.reject(response.data);
            }
        }, function(response){
            // Error occurs getting URL
            console.log(response);
            deferredResponse.reject('There was problem with the network. Please check your network connectivity and try again.')
        });
        return deferredResponse.promise;
    }
}]);