// static/js/signUpFormController.js
angular.module('jobPortalApp', [])
    .controller('FormController', function($scope, $http) {
        $scope.user = {};

        $scope.submitForm = function(isValid) {
            if (isValid) {
                $http.post('/signup/', $scope.user)
                    .then(function(response) {
                        console.log('Signup successful:', response.data);
                        alert('Signup successful! Please log in.');
                    }, function(error) {
                        console.error('Signup error:', error);
                        alert('Error during signup. Please try again.');
                    });
            }
        };
    });
