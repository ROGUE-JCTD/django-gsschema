var app = angular.module('gsschema',['ngCookies']);

if(!String.prototype.startsWith){
    String.prototype.startsWith = function (str) {
        return !this.indexOf(str);
    }
}

app.controller('gsschema_ctrl', function($scope, $http, $q, $cookies, fileUpload){
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
			    //$(xhr.data).find('ServiceException').attr("ServiceException");
            } else {
                // TODO: indicate that retrieving the layers has failed.
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
        console.log('file is ' );
        console.dir(file);

        // Parse XML for errors

        if (window.DOMParser){ // All browsers except IE before ver. 9
            var Parser = new DOMParser();
            try{
                var xmlDoc = Parser.parseFromString(file, "text/xml");
            } catch(e){
                window.alert("Error creating XML: {}".format(e.message));
            }
        } else {
            xmlDoc = CreateMSXMLDocumentObject();
            if (!xmlDoc) {
                window.alert("Cannot create XMLDocument object");
            }
            xmlDoc.loadXML(file);
        }

        var errorMsg = null;
        if (xmlDoc.parseError && xmlDoc.parseError.errorCode != 0){
            errorMsg = "XML Parsing Error: " + xmlDoc.parseError.reason
                + " at line " + xmlDoc.parseError.line
                + " at position " + xmlDoc.parseError.linepos;
        } else {
            if (xmlDoc.documentElement) {
                if (xmlDoc.documentElement.firstChild.firstChild.nodeName == "parsererror") {
                    errorMsg = xmlDoc.documentElement.childNodes[0].innerHTML;
                }
            } else {
                errorMsg = "XML Parsing Error: unknown?";
            }
        }

        if (errorMsg){
            window.alert(errorMsg);
        }

        console.log(xmlFile);

        var uploadUrl = "/fileUpload";
        fileUpload.uploadFileToUrl(file, '/gsschema/' + $scope.layerSelector + '/upload', $cookies.get('csrftoken'));
    };

    $scope.remove = function() {
        var confirm = window.confirm("Are you sure you want to remove the file?");
        if (confirm === true) {
            // OK
            var removeUrl = '/gsschema/' + $scope.layerSelector + '/remove/';
            window.location = removeUrl;
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
                    scope.hasUploadFile = true;
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
      } else if (attrs.toggle=="popover"){
        // I don't think this works
        $(element).popover();
      }
    }
  };
})

app.service('fileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function(file, uploadUrl, csrfToken){
        var formData = new FormData();
        formData.append('file', file);
        console.log(file);
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
    };
}]);